from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config
import atexit

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
                
        # Register cleanup when the module is loaded
        atexit.register(self.close)
    
    def connect(self):
        try:
            self.client = MongoClient(Config.MONGODB_URL, serverSelectionTimeoutMS=5000)
            self.db = self.client[Config.DB_NAME]
            # Test connection
            self.client.admin.command('ping')
            print("Connected to MongoDB")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            exit(1)
    
    
    def get_collection(self, name):
        return self.db[name]

    
    def close(self):
        if self.client:
            self.client.close()
            self.client = None


# Singleton instance
db = MongoDB()
