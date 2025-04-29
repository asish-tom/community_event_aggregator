import os
import time
import schedule
from typing import List
from dotenv import load_dotenv
from src.models.event import Event
from src.models.user_preferences import UserPreferences
from src.sources.web_scraper import CommunityWebScraper
from src.services.event_processor import EventProcessor

# Load environment variables
load_dotenv()

def create_event_sources() -> List[CommunityWebScraper]:
    """Initialize event sources"""
    sources = [
        CommunityWebScraper(os.getenv('COMMUNITY_EVENTS_URL', 'http://example.com/events'))
        # Add more sources here as needed
    ]
    return sources

def load_user_preferences() -> List[UserPreferences]:
    """Load user preferences - could be expanded to load from database"""
    # Example user preferences
    return [
        UserPreferences(
            user_id="1",
            categories=["music", "arts", "technology"],
            locations=["downtown", "midtown"],
            email="user@example.com"
        )
    ]

def setup_event_processor() -> EventProcessor:
    """Initialize event processor with SMTP configuration"""
    smtp_config = {
        'host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
        'port': os.getenv('SMTP_PORT', '587'),
        'username': os.getenv('SMTP_USERNAME', ''),
        'password': os.getenv('SMTP_PASSWORD', '')
    }
    return EventProcessor(smtp_config)

def process_events(sources: List[CommunityWebScraper], 
                  processor: EventProcessor,
                  users: List[UserPreferences]):
    """Fetch and process events for all users"""
    print("Fetching and processing events...")
    
    # Fetch events from all sources
    all_events = []
    for source in sources:
        try:
            events = source.fetch_events()
            all_events.extend(events)
        except Exception as e:
            print(f"Error fetching events from source: {e}")
    
    # Update processor's event cache
    processor.update_events(all_events)
    
    # Process events for each user
    for user in users:
        matching_events = processor.get_matching_events(user)
        if matching_events and user.notification_preferences.get('email'):
            processor.send_email_notification(user, matching_events)

def main():
    """Main application entry point"""
    print("Starting the Community Event Aggregator...")
    
    # Initialize components
    sources = create_event_sources()
    processor = setup_event_processor()
    users = load_user_preferences()
    
    # Schedule event processing
    schedule.every(1).hours.do(
        process_events, 
        sources=sources, 
        processor=processor, 
        users=users
    )
    
    # Initial run
    process_events(sources, processor, users)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()