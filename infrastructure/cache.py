import time
from functools import wraps
from config import Config

class Cache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value, ttl=None):
        if ttl is None:
            ttl = Config.CACHE_TTL
        expiry = time.time() + ttl
        self.cache[key] = (value, expiry)
    
    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        self.cache.clear()

# Singleton instance
cache = Cache()

def cached(ttl=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Create a cache key based on function name and arguments
            cache_key = f"{f.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            result = f(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
