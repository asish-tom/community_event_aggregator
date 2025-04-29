from abc import ABC, abstractmethod
from typing import List
from src.models.event import Event

class EventSource(ABC):
    """Base interface for event sources"""
    
    @abstractmethod
    def fetch_events(self) -> List[Event]:
        """Fetch events from the source"""
        pass
    
    @abstractmethod
    def validate_event(self, event: Event) -> bool:
        """Validate event data"""
        if not event.title or not event.date or not event.location:
            return False
        return True
    
    def standardize_location(self, location: str) -> str:
        """Standardize location format"""
        # Basic implementation - could be enhanced with geocoding
        return location.strip().lower()
    
    def parse_date(self, date_str: str):
        """Helper method to parse dates in various formats"""
        # To be implemented by specific sources based on their date formats
        raise NotImplementedError
    
    def clean_text(self, text: str) -> str:
        """Clean and standardize text fields"""
        if not text:
            return ""
        return " ".join(text.strip().split())