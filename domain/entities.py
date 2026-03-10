from datetime import datetime
from bson import ObjectId
import pytz

class User:
    def __init__(self, name,phone,country, pinHash, isAdmin, created_at=None, _id=None):
        self._id = _id or ObjectId()
        self.name = name
        self.phone =phone
        self.country=country
        self.pinHash= pinHash
        self.isAdmin = isAdmin
        self.created_at = created_at or datetime.now(pytz.UTC)
    
    def to_dict(self):
        return {
            "_id": self._id,
            "name":self.name,
            "phone": self.phone,
            "country": self.country,
            "pinHash":self.pinHash,
            "isAdmin":self.isAdmin,
            "created_at": self.created_at
        }

class Chat:
    def __init__(self, content, owner_id, timestamp=None, _id=None):
        self._id = _id or ObjectId()
        self.content = content
        self.owner_id = owner_id
        self.timestamp = timestamp or datetime.now(pytz.UTC)
    
    def to_dict(self):
        return {
            "_id": self._id,
            "content": self.content,
            "owner_id": self.owner_id,
            "timestamp": self.timestamp
        }

class Settings:
    def __init__(self, user_id, theme="light", notifications="enabled", _id=None):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.theme = theme
        self.notifications = notifications
    
    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "theme": self.theme,
            "notifications": self.notifications
        }
