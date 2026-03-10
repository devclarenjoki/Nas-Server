from infrastructure.database import db
from infrastructure.cache import cache
from infrastructure.auth import get_pin_hash
from domain.entities import User, Chat, Settings

class UserService:
    @staticmethod
    async def create_user(name,phone,country, pin,isAdmin):
        hashed_pin = get_pin_hash(pin)
        user = User(name,phone,country, hashed_pin,isAdmin)
        result = db.get_collection("users").insert_one(user.to_dict())
        
        # Create default settings
        settings = Settings(result.inserted_id)
        db.get_collection("settings").insert_one(settings.to_dict())
        
        # Clear cache
        cache.clear()
        return result.inserted_id
    
    # @staticmethod
    # async def get_user_by_username(username):
    #     user_data = db.get_collection("users").find_one({"username": username})
    #     if user_data:
    #         return User(
    #             email=user_data["email"],
    #             username=user_data["username"],
    #             hashed_password=user_data["hashed_password"],
    #             created_at=user_data["created_at"],
    #             _id=user_data["_id"]
    #         )
    #     return None

    @staticmethod
    async def get_user_by_phone(phone):
        user_data = db.get_collection("users").find_one({"phone": phone})
        if user_data:
            return User(
                name=user_data["name"],
                phone=user_data["phone"],
                country=user_data["country"],
                pinHash=user_data["pinHash"],
                isAdmin=user_data["isAdmin"],
                created_at=user_data["created_at"],
                _id=user_data["_id"]
            )
        return None
    
    @staticmethod
    async def get_user_by_id(user_id):
        user_data = db.get_collection("users").find_one({"_id": user_id})
        if user_data:
            return User(
                name=user_data["name"],
                phone=user_data["phone"],
                country=[user_data["country"]],
                pinHash=user_data["pinHash"],
                isAdmin=user_data['isAdmin'],
                created_at=user_data["created_at"],
                _id=user_data["_id"]
            )
        return None

class ChatService:
    @staticmethod
    async def create_chat(content, owner_id):
        chat = Chat(content, owner_id)
        result = db.get_collection("chats").insert_one(chat.to_dict())
        
        # Clear cache for this user's chats
        cache.delete(f"chats:{owner_id}")
        return result.inserted_id
    
    @staticmethod
    def get_user_chats(owner_id):
        # Check cache first
        cached_chats = cache.get(f"chats:{owner_id}")
        if cached_chats:
            return cached_chats
        
        chats = list(db.get_collection("chats").find({"owner_id": owner_id}).sort("timestamp", -1))
        for chat in chats:
            chat["id"] = str(chat["_id"])
            chat["owner_id"]=str(chat["owner_id"])
            #chat["timestamp"] = chat["timestamp"].isoformat()
            chat["timestamp"] = chat["timestamp"].strftime("%Y-%m-%d%H:%M:%S")

            
            del chat["_id"]
        
        # Cache the result
        cache.set(f"chats:{owner_id}", chats)

        #print(chats)
        return chats

    
    @staticmethod
    def get_user_chat(owner_id,chat_id):
        # Check cache first
        cached_chat = cache.get(f"chats:{owner_id}{chat_id}")
        if cached_chat:
            return cached_chat
        
        chat = db.get_collection("chats").find_one({"_id":chat_id})

        chat2 = {}
        
        chat2["id"] = str(chat["_id"])
        chat2["content"]=chat["content"]
        chat2["owner_id"]=str(chat["owner_id"])
        
            #chat["timestamp"] = chat["timestamp"].isoformat()
        chat2["timestamp"] = chat["timestamp"].strftime("%Y-%m-%d%H:%M:%S")

        
            
            #del chata["_id"]
        
        # Cache the result
        cache.set(f"chats:{owner_id}{chat_id}", chat)

        #print(chats)
        return chat2
    
    @staticmethod
    def delete_chat(chat_id, owner_id):
        result = db.get_collection("chats").delete_one({
            "_id": chat_id,
            "owner_id": owner_id
        })
        
        if result.deleted_count > 0:
            # Clear cache for this user's chats
            cache.delete(f"chats:{owner_id}")
            return True
        return False

class SettingsService:
    @staticmethod
    async def get_settings(user_id):
        # Check cache first
        cached_settings = cache.get(f"settings:{user_id}")
        if cached_settings:
            return cached_settings
        
        settings = db.get_collection("settings").find_one({"user_id": user_id})
        if settings:
            result = {
                "theme": settings["theme"],
                "notifications": settings["notifications"]
            }
            # Cache the result
            cache.set(f"settings:{user_id}", result)
            return result
        return None
    
    @staticmethod
    async def update_settings(user_id, theme=None, notifications=None):
        update_data = {}
        if theme is not None:
            update_data["theme"] = theme
        if notifications is not None:
            update_data["notifications"] = notifications
        
        if not update_data:
            return False
        
        result = db.get_collection("settings").update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            # Clear cache for this user's settings
            cache.delete(f"settings:{user_id}")
            return True
        return False
