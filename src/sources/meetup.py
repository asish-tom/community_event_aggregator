import os
import requests
from datetime import datetime
from typing import List
import time
from src.sources.base import EventSource
from src.models.event import Event

class MeetupSource(EventSource):
    """Event source for Meetup.com API"""
    
    def __init__(self):
        self.api_key = os.getenv('MEETUP_API_KEY')
        if not self.api_key:
            raise ValueError("MEETUP_API_KEY environment variable is required")
        
        self.base_url = "https://api.meetup.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        })
    
    def fetch_events(self) -> List[Event]:
        """Fetch events from Meetup.com API"""
        try:
            # Get events for specified location/topic
            endpoint = f"{self.base_url}/find/upcoming_events"
            params = {
                'page': 20,  # Number of results
                'fields': 'group_key_photo',  # Include group photo
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
                    print(f"Error parsing Meetup event: {e}")
                    continue
                    
            return events
            
        except requests.RequestException as e:
            print(f"Error fetching Meetup events: {e}")
            return []
    
    def _parse_event(self, event_data: dict) -> Event:
        """Parse event data from Meetup API response"""
        venue = event_data.get('venue', {})
        group = event_data.get('group', {})
        
        return Event(
            id=event_data['id'],
            title=event_data['name'],
            description=event_data.get('description', ''),
            date=datetime.fromtimestamp(event_data['time'] / 1000),
            location=f"{venue.get('name', 'TBD')} - {venue.get('city', 'Unknown')}",
            category=group.get('category', {}).get('name', 'Other'),
            source="meetup",
            url=event_data.get('link'),
            image_url=group.get('key_photo', {}).get('photo_link')
        )
    
    def validate_event(self, event: Event) -> bool:
        """Additional validation for Meetup events"""
        if not super().validate_event(event):
            return False
        
        # Add Meetup-specific validation
        if not event.url or 'meetup.com' not in event.url:
            return False
            
        return True
    
    def parse_date(self, date_str: str) -> datetime:
        """Parse date from Meetup API (not used as we get timestamp)"""
        raise NotImplementedError("Meetup API provides timestamps directly")