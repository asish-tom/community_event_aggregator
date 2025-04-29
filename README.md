# Community Event Aggregator

A Python-based system that aggregates local community events from various online sources, filters them based on user preferences, and provides personalized notifications.

## Supported Event Sources

The system can be configured to scrape events from various sources:

1. Meetup.com (using their API):
   - Requires API key from https://www.meetup.com/api/
   - Rate limits: 30 requests/hour for basic tier
   - Example configuration in .env:
     ```
     MEETUP_API_KEY=your_api_key_here
     ```

2. Eventbrite (using their API):
   - Requires API key from https://www.eventbrite.com/platform/
   - Rate limits: 1000 requests/hour
   - Example configuration:
     ```
     EVENTBRITE_API_KEY=your_api_key_here
     ```

3. Local community websites:
   - City event calendars
   - Local venues' websites
   - Community center schedules
   - Note: Always check robots.txt and terms of service before scraping

### Adding New Sources

To add a new event source:

1. Create a new class in `src/sources/` that inherits from `EventSource`
2. Implement the required methods:
   - `fetch_events()`
   - `validate_event()`
   - `parse_date()`

Example:
```python
from src.sources.base import EventSource

class MyNewSource(EventSource):
    def fetch_events(self):
        # Implementation for fetching events
        pass
```

### Ethical Scraping Guidelines

When adding new sources:
1. Check the website's robots.txt file
2. Respect rate limiting and crawling policies
3. Consider using official APIs when available
4. Add appropriate delays between requests
5. Cache results when possible
6. Keep data usage minimal and relevant

## Features

- Web scraping/API integration for event collection
- User preference management
- Event filtering and matching
- Email notification system
- High test coverage (98%)

[Rest of README content remains the same...]