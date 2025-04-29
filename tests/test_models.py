import pytest
from datetime import datetime
from src.models.event import Event
from src.models.user_preferences import UserPreferences

def test_event_creation():
    """Test Event model creation and methods"""
    event = Event(
        id="123",
        title="Tech Meetup",
        description="Monthly technology meetup",
        date=datetime(2024, 1, 1, 18, 30),
        location="downtown",
        category="technology",
        source="test",
        url="http://example.com"
    )
    
    assert event.id == "123"
    assert event.title == "Tech Meetup"
    assert event.category == "technology"
    
    # Test to_dict method
    event_dict = event.to_dict()
    assert event_dict['title'] == "Tech Meetup"
    assert event_dict['date'] == "2024-01-01T18:30:00"
    
    # Test from_dict method
    new_event = Event.from_dict(event_dict)
    assert new_event.title == event.title
    assert new_event.date.year == 2024
    assert new_event.date.month == 1

def test_user_preferences_creation():
    """Test UserPreferences model creation and methods"""
    prefs = UserPreferences(
        user_id="user1",
        categories=["technology", "music"],
        locations=["downtown"],
        email="test@example.com"
    )
    
    assert prefs.user_id == "user1"
    assert "technology" in prefs.categories
    assert len(prefs.locations) == 1
    
    # Test to_dict method
    prefs_dict = prefs.to_dict()
    assert prefs_dict['user_id'] == "user1"
    assert "technology" in prefs_dict['categories']
    
    # Test from_dict method
    new_prefs = UserPreferences.from_dict(prefs_dict)
    assert new_prefs.user_id == prefs.user_id
    assert new_prefs.categories == prefs.categories

def test_event_matching():
    """Test event matching with user preferences"""
    prefs = UserPreferences(
        user_id="user1",
        categories=["technology"],
        locations=["downtown"]
    )
    
    matching_event = Event(
        id="123",
        title="Tech Meetup",
        description="A tech event",
        date=datetime.now(),
        location="downtown",
        category="technology",
        source="test"
    )
    
    non_matching_event = Event(
        id="124",
        title="Music Festival",
        description="A music event",
        date=datetime.now(),
        location="uptown",
        category="music",
        source="test"
    )
    
    assert prefs.matches_event(matching_event) == True
    assert prefs.matches_event(non_matching_event) == False

def test_notification_preferences():
    """Test notification preferences management"""
    prefs = UserPreferences(
        user_id="user1",
        notification_preferences={
            "email": True,
            "dashboard": False
        }
    )
    
    assert prefs.notification_preferences["email"] == True
    assert prefs.notification_preferences["dashboard"] == False
    
    # Test dictionary conversion
    prefs_dict = prefs.to_dict()
    assert prefs_dict["notification_preferences"]["email"] == True

def test_user_preferences_default_values():
    """Test UserPreferences default values"""
    prefs = UserPreferences(user_id="user1")
    
    # Test default values
    assert prefs.categories == []
    assert prefs.locations == []
    assert prefs.max_distance == 50.0
    assert prefs.notification_preferences == {"email": True, "dashboard": True}
    assert prefs.email is None