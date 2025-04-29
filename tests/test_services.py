import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from src.models.event import Event
from src.models.user_preferences import UserPreferences
from src.services.event_processor import EventProcessor

@pytest.fixture
def sample_events():
    """Fixture providing sample events"""
    return [
        Event(
            id="1",
            title="Tech Conference",
            description="Annual tech conference",
            date=datetime.now() + timedelta(days=1),
            location="downtown",
            category="technology",
            source="test"
        ),
        Event(
            id="2",
            title="Music Festival",
            description="Local music festival",
            date=datetime.now() + timedelta(days=2),
            location="park",
            category="music",
            source="test"
        )
    ]

@pytest.fixture
def sample_preferences():
    """Fixture providing sample user preferences"""
    return UserPreferences(
        user_id="user1",
        categories=["technology"],
        locations=["downtown"],
        email="test@example.com"
    )

@pytest.fixture
def event_processor():
    """Fixture providing EventProcessor instance"""
    smtp_config = {
        'host': 'smtp.example.com',
        'port': '587',
        'username': 'test@example.com',
        'password': 'password'
    }
    return EventProcessor(smtp_config)

def test_event_filtering(event_processor, sample_events, sample_preferences):
    """Test filtering events based on user preferences"""
    # Update processor with sample events
    event_processor.update_events(sample_events)
    
    # Get matching events
    matching_events = event_processor.get_matching_events(sample_preferences)
    
    # Should only match the tech conference
    assert len(matching_events) == 1
    assert matching_events[0].title == "Tech Conference"

def test_cache_update_check(event_processor):
    """Test cache update checking logic"""
    # Initially should need update
    assert event_processor.should_update_cache() == True
    
    # Update events
    event_processor.update_events([])
    
    # Should not need immediate update
    assert event_processor.should_update_cache() == False
    
    # Should need update after time passes
    event_processor._last_update -= timedelta(hours=2)
    assert event_processor.should_update_cache() == True

@patch('smtplib.SMTP')
def test_email_notification(mock_smtp, event_processor, sample_events, sample_preferences):
    """Test email notification sending"""
    # Configure mock
    mock_smtp_instance = Mock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    
    # Update processor with events
    event_processor.update_events(sample_events)
    
    # Get matching events and send notification
    matching_events = event_processor.get_matching_events(sample_preferences)
    event_processor.send_email_notification(sample_preferences, matching_events)
    
    # Verify SMTP interactions
    mock_smtp.assert_called_once_with(
        event_processor.smtp_config['host'],
        int(event_processor.smtp_config['port'])
    )
    assert mock_smtp_instance.starttls.called
    assert mock_smtp_instance.login.called
    assert mock_smtp_instance.send_message.called

def test_email_formatting(event_processor, sample_events):
    """Test email body formatting"""
    # Get formatted email body
    email_body = event_processor._format_email_body(sample_events)
    
    # Check for expected content
    assert "Tech Conference" in email_body
    assert "Music Festival" in email_body
    assert "Location:" in email_body
    assert "Date:" in email_body
    
    # Check HTML formatting
    assert "<html>" in email_body
    assert "</html>" in email_body
    assert "<h2>" in email_body

def test_empty_events_handling(event_processor, sample_preferences):
    """Test handling of empty events list"""
    event_processor.update_events([])
    matching_events = event_processor.get_matching_events(sample_preferences)
    
    assert len(matching_events) == 0

@patch('smtplib.SMTP')
def test_notification_error_handling(mock_smtp, event_processor, sample_events, sample_preferences):
    """Test error handling in notification sending"""
    # Configure mock to raise an exception
    mock_smtp.side_effect = Exception("SMTP Error")
    
    # Should not raise exception
    event_processor.send_email_notification(sample_preferences, sample_events)

def test_notification_empty_user_email(event_processor, sample_events):
    """Test notification handling with empty user email"""
    prefs = UserPreferences(user_id="user1")  # No email set
    event_processor.send_email_notification(prefs, sample_events)
    # Should not raise any exception