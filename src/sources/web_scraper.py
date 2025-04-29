import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import uuid
from src.sources.base import EventSource
from src.models.event import Event

class CommunityWebScraper(EventSource):
    """Example web scraper for community events"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_events(self) -> List[Event]:
        """Fetch events from the community website"""
        try:
            response = self.session.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            events = []
            # Example: looking for event cards/containers
            event_elements = soup.find_all('div', class_='event-card')
            
            for element in event_elements:
                try:
                    event = self._parse_event(element)
                    if self.validate_event(event):
                        events.append(event)
                except Exception as e:
                    print(f"Error parsing event: {e}")
                    continue
                    
            return events
            
        except requests.RequestException as e:
            print(f"Error fetching events: {e}")
            return []
    
    def _parse_event(self, element: BeautifulSoup) -> Event:
        """Parse event data from HTML element"""
        # Example parsing logic - adjust based on actual HTML structure
        title = element.find('h2', class_='event-title').text.strip()
        description = element.find('p', class_='event-description').text.strip()
        date_str = element.find('span', class_='event-date').text.strip()
        location = element.find('span', class_='event-location').text.strip()
        category = element.find('span', class_='event-category').text.strip()
        
        # Handle optional URL field
        url_element = element.find('a', class_='event-link')
        url = url_element['href'] if url_element else None
        
        return Event(
            id=str(uuid.uuid4()),
            title=self.clean_text(title),
            description=self.clean_text(description),
            date=self.parse_date(date_str),
            location=self.standardize_location(location),
            category=category.lower(),
            source="community_web",
            url=url
        )
    
    def parse_date(self, date_str: str) -> datetime:
        """Parse date string into datetime object"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                # Try alternative format
                return datetime.strptime(date_str, "%B %d, %Y %I:%M %p")
            except ValueError:
                raise ValueError(f"Unable to parse date: {date_str}")
    
    def validate_event(self, event: Event) -> bool:
        """Additional validation specific to this source"""
        if not super().validate_event(event):
            return False
        
        # Add source-specific validation
        if len(event.description) < 10:  # Arbitrary minimum description length
            return False
            
        return True