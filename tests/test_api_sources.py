import pytest
from datetime import datetime
from unittest.mock import Mock, patch
import requests
from src.sources.meetup import MeetupSource
from src.sources.eventbrite import EventbriteSource

@pytest.fixture
def meetup_response():
    """Sample Meetup API response"""
    return {
        "events": [{
            "id": "123",
            "name": "Python Meetup",
            "description": "Monthly Python programming meetup",
            "time": 1714500000000,  # Example timestamp
            "venue": {
                "name": "Tech Hub",
                "city": "New York"
            },
            "group": {
                "category": {
                    "name": "Technology"
                },
                "key_photo": {
                    "photo_link": "http://example.com/photo.jpg"
                }
            },
            "link": "http://meetup.com/event/123"
        }]
    }

@pytest.fixture
def eventbrite_response():
    """Sample Eventbrite API response"""
    return {
        "events": [{
            "id": "456",
            "name": {"text": "Tech Conference"},
            "description": {"text": "Annual technology conference"},
            "start": {
                "local": "2024-05-01T09:00:00",
                "utc": "2024-05-01T13:00:00Z"
            },
            "venue": {
                "name": "Convention Center",
                "address": {"city": "New York"}
            },
            "category": {
                "name": "Technology"
            },
            "url": "http://eventbrite.com/e/456",
            "logo": {
                "url": "http://example.com/logo.jpg"
            }
        }]
    }

@patch.dict('os.environ', {'MEETUP_API_KEY': 'fake_key'})
def test_meetup_source(meetup_response):
    """Test Meetup event source"""
    source = MeetupSource()
    
    # Mock the API response
    mock_response = Mock()
    mock_response.json.return_value = meetup_response
    source.session.get = Mock(return_value=mock_response)
    
    # Fetch events
    events = source.fetch_events()
    
    assert len(events) == 1
    event = events[0]
    
    assert event.id == "123"
    assert event.title == "Python Meetup"
    assert event.category == "Technology"
    assert "Tech Hub" in event.location
    assert event.source == "meetup"
    assert "meetup.com" in event.url

@patch.dict('os.environ', {'EVENTBRITE_API_KEY': 'fake_key'})
def test_eventbrite_source(eventbrite_response):
    """Test Eventbrite event source"""
    source = EventbriteSource()
    
    # Mock the API response
    mock_response = Mock()
    mock_response.json.return_value = eventbrite_response
    source.session.get = Mock(return_value=mock_response)
    
    # Fetch events
    events = source.fetch_events()
    
    assert len(events) == 1
    event = events[0]
    
    assert event.id == "456"
    assert event.title == "Tech Conference"
    assert event.category == "Technology"
    assert "Convention Center" in event.location
    assert event.source == "eventbrite"
    assert "eventbrite.com" in event.url

def test_missing_meetup_api_key():
    """Test Meetup source without API key"""
    with patch.dict('os.environ', clear=True):
        with pytest.raises(ValueError) as excinfo:
            MeetupSource()
        assert "MEETUP_API_KEY" in str(excinfo.value)

def test_missing_eventbrite_api_key():
    """Test Eventbrite source without API key"""
    with patch.dict('os.environ', clear=True):
        with pytest.raises(ValueError) as excinfo:
            EventbriteSource()
        assert "EVENTBRITE_API_KEY" in str(excinfo.value)

@patch.dict('os.environ', {'MEETUP_API_KEY': 'fake_key'})
def test_meetup_api_error():
    """Test Meetup API error handling"""
    source = MeetupSource()
    source.session.get = Mock(side_effect=requests.RequestException("API Error"))
    
    events = source.fetch_events()
    assert len(events) == 0

@patch.dict('os.environ', {'EVENTBRITE_API_KEY': 'fake_key'})
def test_eventbrite_api_error():
    """Test Eventbrite API error handling"""
    source = EventbriteSource()
    source.session.get = Mock(side_effect=requests.RequestException("API Error"))
    
    events = source.fetch_events()
    assert len(events) == 0

@patch.dict('os.environ', {'MEETUP_API_KEY': 'fake_key'})
def test_meetup_invalid_response():
    """Test handling of invalid Meetup API response"""
    source = MeetupSource()
    
    # Mock response with missing required fields
    mock_response = Mock()
    mock_response.json.return_value = {"events": [{"id": "123"}]}  # Missing required fields
    source.session.get = Mock(return_value=mock_response)
    
    events = source.fetch_events()
    assert len(events) == 0

@patch.dict('os.environ', {'EVENTBRITE_API_KEY': 'fake_key'})
def test_eventbrite_invalid_response():
    """Test handling of invalid Eventbrite API response"""
    source = EventbriteSource()
    
    # Mock response with missing required fields
    mock_response = Mock()
    mock_response.json.return_value = {"events": [{"id": "456"}]}  # Missing required fields
    source.session.get = Mock(return_value=mock_response)
    
    events = source.fetch_events()
    assert len(events) == 0