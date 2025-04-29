from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class UserPreferences:
    """Stores user preferences for event filtering"""
    user_id: str
    categories: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    max_distance: float = 50.0  # in kilometers
    notification_preferences: Dict[str, bool] = field(default_factory=lambda: {
        "email": True,
        "dashboard": True
    })
    email: str = None
    
    def to_dict(self):
        """Convert preferences to dictionary format"""
        return {
            'user_id': self.user_id,
            'categories': self.categories,
            'locations': self.locations,
            'max_distance': self.max_distance,
            'notification_preferences': self.notification_preferences,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create a UserPreferences instance from a dictionary"""
        return cls(**data)
    
    def matches_event(self, event) -> bool:
        """Check if an event matches user preferences"""
        # Category matching
        if self.categories and event.category not in self.categories:
            return False
            
        # Location matching (basic implementation)
        if self.locations and event.location not in self.locations:
            return False
            
        return True