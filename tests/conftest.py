import os
import pytest
from datetime import datetime, timedelta
from src.models.event import Event
from src.models.user_preferences import UserPreferences

@pytest.fixture(scope="session")
def smtp_config():
    """Shared SMTP configuration for testing"""
    return {
        'host': 'smtp.example.com',
        'port': '587',
        'username': 'test@example.com',
        'password': 'password'
    }

@pytest.fixture(scope="session")
def base_url():
    """Base URL for web scraper testing"""
    return "http://example.com/events"

@pytest.fixture(scope="function")
def future_datetime():
    """Generate a future datetime for testing"""
    return datetime.now() + timedelta(days=1)

@pytest.fixture(scope="function")
def mock_environment(monkeypatch):
    """Setup mock environment variables for testing"""
    monkeypatch.setenv('COMMUNITY_EVENTS_URL', 'http://example.com/events')
    monkeypatch.setenv('SMTP_HOST', 'smtp.example.com')
    monkeypatch.setenv('SMTP_PORT', '587')
    monkeypatch.setenv('SMTP_USERNAME', 'test@example.com')
    monkeypatch.setenv('SMTP_PASSWORD', 'password')