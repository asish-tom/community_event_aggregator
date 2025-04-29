import os
import requests
from datetime import datetime
from typing import List
import time
from src.sources.base import EventSource
from src.models.event import Event

class EventbriteSource(EventSource):
    """Event source for Eventbrite API"""
    
    def __init__(self):
        self.api_key = os.getenv('EVENTBRITE_API_KEY')
        if not self.api_key:
            raise ValueError("EVENTBRITE_API_KEY environment variable is required")
        
        self.base_url = "https://www.eventbriteapi.com/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        })
    
    def fetch_events(self) -> List[Event]:
        """Fetch events from Eventbrite API"""
        try:
            # Search for events
            endpoint = f"{self.base_url}/events/search/"
            params = {
                'expand': 'venue,category',  # Include venue and category details
                'status': 'live',           # Only live events
                'sort_by': 'date',
            }
            
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            events = []
            for event_data in data.get('events', []):
                try:
                    event = self._parse_event(event_data)
                    if self.validate_event(event):
                        events.append(event)
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    print(f"Error parsing Eventbrite event: {e}")
                    continue
                    
            return events
            
        except requests.RequestException as e:
            print(f"Error fetching Eventbrite events: {e}")
            return []
    
    def _parse_event(self, event_data: dict) -> Event:
        """Parse event data from Eventbrite API response"""
        venue = event_data.get('venue', {})
        category = event_data.get('category', {})
        
        # Parse start date and time
        start = event_data.get('start', {})
        if 'local' in start:
            event_date = datetime.fromisoformat(start['local'])
        else:
            event_date = datetime.fromisoformat(start['utc'])
        
        return Event(
            id=event_data['id'],
            title=event_data['name']['text'],
            description=event_data['description']['text'],
            date=event_date,
            location=f"{venue.get('name', 'TBD')} - {venue.get('address', {}).get('city', 'Unknown')}",
            category=category.get('name', 'Other'),
            source="eventbrite",
            url=event_data.get('url'),
            image_url=event_data.get('logo', {}).get('url')
        )
    
    def validate_event(self, event: Event) -> bool:
        """Additional validation for Eventbrite events"""
        if not super().validate_event(event):
            return False
        
        # Add Eventbrite-specific validation
        if not event.url or 'eventbrite' not in event.url:
            return False
            
        return True
    
    def parse_date(self, date_str: str) -> datetime:
        """Parse date from Eventbrite API (not used as we get ISO format)"""
        raise NotImplementedError("Eventbrite API provides dates in ISO format")