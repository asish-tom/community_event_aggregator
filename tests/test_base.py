import pytest
from datetime import datetime
from src.models.event import Event
from src.sources.base import EventSource

class TestEventSource(EventSource):
    """Test implementation of EventSource"""
    def fetch_events(self):
        return []
        
    def validate_event(self, event):
        return super().validate_event(event)

def test_base_validate_event():
    """Test the base validation logic"""
    source = TestEventSource()
    
    # Test valid event
    valid_event = Event(
        id="1",
        title="Test Event",
        description="Description",
        date=datetime.now(),
        location="Test Location",
        category="test",
        source="test"
    )
    assert source.validate_event(valid_event) == True
    
    # Test invalid event (missing required fields)
    invalid_event = Event(
        id="2",
        title="",  # Empty title
        description="Description",
        date=datetime.now(),
        location="Test Location",
        category="test",
        source="test"
    )
    assert source.validate_event(invalid_event) == False

def test_parse_date():
    """Test the base parse_date method"""
    source = TestEventSource()
    with pytest.raises(NotImplementedError):
        source.parse_date("2024-01-01")

def test_clean_text():
    """Test text cleaning in base class"""
    source = TestEventSource()
    assert source.clean_text(" Test Text  ") == "Test Text"
    assert source.clean_text(None) == ""
    assert source.clean_text("Multiple   Spaces") == "Multiple Spaces"