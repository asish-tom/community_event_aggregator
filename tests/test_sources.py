import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
import requests
from src.sources.web_scraper import CommunityWebScraper

@pytest.fixture
def sample_html():
    """Fixture providing sample HTML for testing"""
    return """
    <div class="event-card">
        <h2 class="event-title">Python Meetup</h2>
        <p class="event-description">Monthly Python programming meetup</p>
        <span class="event-date">2024-01-01 18:30</span>
        <span class="event-location">Downtown Tech Hub</span>
        <span class="event-category">Technology</span>
        <a class="event-link" href="http://example.com/event1">Details</a>
    </div>
    <div class="event-card">
        <h2 class="event-title">Art Workshop</h2>
        <p class="event-description">Beginner's art workshop</p>
        <span class="event-date">2024-01-02 14:00</span>
        <span class="event-location">Community Center</span>
        <span class="event-category">Arts</span>
        <a class="event-link" href="http://example.com/event2">Details</a>
    </div>
    """

@pytest.fixture
def web_scraper():
    """Fixture providing CommunityWebScraper instance"""
    return CommunityWebScraper("http://example.com/events")

def test_fetch_events(web_scraper, sample_html):
    """Test event fetching and parsing"""
    # Configure mock response
    mock_response = Mock()
    mock_response.text = sample_html
    mock_response.raise_for_status = Mock()
    
    # Mock the session's get method
    web_scraper.session.get = Mock(return_value=mock_response)
    
    # Fetch events
    events = web_scraper.fetch_events()
    
    # Verify request
    web_scraper.session.get.assert_called_once_with(
        "http://example.com/events",
        headers=web_scraper.headers
    )
    
    # Verify parsed events
    assert len(events) == 2
    
    event1, event2 = events
    
    assert event1.title == "Python Meetup"
    assert event1.category == "technology"
    assert event1.location == "downtown tech hub"
    
    assert event2.title == "Art Workshop"
    assert event2.category == "arts"
    assert event2.location == "community center"

def test_fetch_events_parsing_error(web_scraper):
    """Test handling of event parsing errors"""
    bad_html = """
    <div class="event-card">
        <h2 class="event-title">Bad Event</h2>
        <!-- Missing required fields -->
    </div>
    """
    mock_response = Mock()
    mock_response.text = bad_html
    mock_response.raise_for_status = Mock()
    web_scraper.session.get = Mock(return_value=mock_response)
    
    events = web_scraper.fetch_events()
    assert len(events) == 0  # Should skip invalid events

def test_request_error_handling(web_scraper):
    """Test handling of request errors"""
    web_scraper.session.get = Mock(side_effect=requests.RequestException("Network error"))
    
    # Should return empty list on error
    events = web_scraper.fetch_events()
    assert len(events) == 0

def test_event_validation(web_scraper):
    """Test event validation logic"""
    soup = BeautifulSoup("""
    <div class="event-card">
        <h2 class="event-title">Test Event</h2>
        <p class="event-description">A</p>
        <span class="event-date">2024-01-01 18:30</span>
        <span class="event-location">Location</span>
        <span class="event-category">Category</span>
    </div>
    """, 'html.parser')
    
    # Event with very short description should be invalid
    event = web_scraper._parse_event(soup.find('div'))
    assert web_scraper.validate_event(event) == False

def test_date_parsing(web_scraper):
    """Test date string parsing"""
    # Test standard format
    date1 = web_scraper.parse_date("2024-01-01 18:30")
    assert isinstance(date1, datetime)
    assert date1.year == 2024
    assert date1.hour == 18
    
    # Test alternative format
    date2 = web_scraper.parse_date("January 01, 2024 06:30 PM")
    assert isinstance(date2, datetime)
    assert date2.year == 2024
    assert date2.hour == 18
    
    # Test invalid format
    with pytest.raises(ValueError):
        web_scraper.parse_date("invalid date format")

def test_location_standardization(web_scraper):
    """Test location standardization"""
    location = web_scraper.standardize_location("  Downtown Tech Hub  ")
    assert location == "downtown tech hub"
    
    location = web_scraper.standardize_location("COMMUNITY center")
    assert location == "community center"

def test_text_cleaning(web_scraper):
    """Test text cleaning functionality"""
    text = web_scraper.clean_text("  Multiple     Spaces   ")
    assert text == "Multiple Spaces"
    
    text = web_scraper.clean_text(None)
    assert text == ""

def test_parse_event_missing_fields(web_scraper):
    """Test handling of missing fields in event parsing"""
    soup = BeautifulSoup("""
    <div class="event-card">
        <h2 class="event-title">Test Event</h2>
        <!-- Missing required fields -->
    </div>
    """, 'html.parser')
    
    with pytest.raises(AttributeError):
        web_scraper._parse_event(soup.find('div'))
