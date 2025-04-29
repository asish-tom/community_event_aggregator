from datetime import datetime
from dataclasses import dataclass

@dataclass
class Event:
    """Represents a community event"""
    id: str
    title: str
    description: str
    date: datetime
    location: str
    category: str
    source: str
    url: str = None
    image_url: str = None
    
    def to_dict(self):
        """Convert event to dictionary format"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat(),
            'location': self.location,
            'category': self.category,
            'source': self.source,
            'url': self.url,
            'image_url': self.image_url
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create an Event instance from a dictionary"""
        if 'date' in data and isinstance(data['date'], str):
            data['date'] = datetime.fromisoformat(data['date'])
        return cls(**data)