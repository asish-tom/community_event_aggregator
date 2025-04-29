from typing import List, Dict
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.models.event import Event
from src.models.user_preferences import UserPreferences

class EventProcessor:
    """Processes events and handles filtering and notifications"""
    
    def __init__(self, smtp_config: Dict[str, str]):
        """
        Initialize with SMTP configuration
        smtp_config should contain: host, port, username, password
        """
        self.smtp_config = smtp_config
        self._cached_events: List[Event] = []
        self._last_update = None
    
    def update_events(self, events: List[Event]):
        """Update the cached events"""
        self._cached_events = events
        self._last_update = datetime.now()
    
    def get_matching_events(self, preferences: UserPreferences) -> List[Event]:
        """Get events matching user preferences"""
        if not self._cached_events:
            return []
            
        matching_events = []
        for event in self._cached_events:
            if preferences.matches_event(event):
                matching_events.append(event)
                
        return matching_events
    
    def send_email_notification(self, user_prefs: UserPreferences, events: List[Event]):
        """Send email notification for matching events"""
        if not events or not user_prefs.email:
            return
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = user_prefs.email
            msg['Subject'] = f"New Community Events Matching Your Interests!"
            
            body = self._format_email_body(events)
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.smtp_config['host'], int(self.smtp_config['port'])) as server:
                server.starttls()
                server.login(self.smtp_config['username'], self.smtp_config['password'])
                server.send_message(msg)
                
        except Exception as e:
            print(f"Error sending email notification: {e}")
    
    def _format_email_body(self, events: List[Event]) -> str:
        """Format events into HTML email body"""
        body = """
        <html>
            <body>
                <h2>New Community Events</h2>
                <p>Here are some events that match your interests:</p>
        """
        
        for event in events:
            body += f"""
                <div style="margin-bottom: 20px;">
                    <h3>{event.title}</h3>
                    <p><strong>Date:</strong> {event.date.strftime('%B %d, %Y %I:%M %p')}</p>
                    <p><strong>Location:</strong> {event.location}</p>
                    <p><strong>Category:</strong> {event.category}</p>
                    <p>{event.description}</p>
                    {'<p><a href="' + event.url + '">More Information</a></p>' if event.url else ''}
                </div>
            """
        
        body += """
            </body>
        </html>
        """
        return body
    
    def should_update_cache(self, max_age_hours: int = 1) -> bool:
        """Check if the event cache needs updating"""
        if not self._last_update:
            return True
            
        age = datetime.now() - self._last_update
        return age > timedelta(hours=max_age_hours)