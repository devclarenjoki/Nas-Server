from infrastructure.database import db
from infrastructure.cache import cache
from datetime import datetime
import pytz
import httpx
from config import Config


class ExchangeRateService:
    
    @staticmethod
    async def fetch_and_store_rates():
        """
        Fetches latest rates from external API and stores them in the database.
        """
        external_url = Config.RATES_API
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(external_url)
                response.raise_for_status() # Raise error for 4xx/5xx responses
                data = response.json()
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            return None

        # Prepare document for MongoDB
        document = {
            "timestamp": data.get("timestamp"),
            "base": data.get("base"),
            "rates": data.get("rates"),
            "fetched_at": datetime.now(pytz.UTC) # Server time when it was fetched
        }
        
        # Insert into 'exchange_rates' collection
        result = db.get_collection("exchange_rates").insert_one(document)
        
        # Invalidate cache for rates
        cache.delete("latest_exchange_rates")
        
        # Return the saved document (converting ObjectId to string for the caller)
        document["_id"] = str(result.inserted_id)
        return document

    @staticmethod
    async def get_latest_rates():
        """Retrieves the most recently stored rates from DB or Cache"""
        cache_key = "latest_exchange_rates"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Get the latest document based on fetched_at timestamp
        doc = db.get_collection("exchange_rates").find_one(
            sort=[("fetched_at", -1)]
        )
        
        if not doc:
            return None
            
        # Format for response
        result = {
            "timestamp": doc.get("timestamp"),
            "base": doc.get("base"),
            "rates": doc.get("rates"),
            "fetched_at": doc["fetched_at"].strftime("%Y-%m-%d %H:%M:%S")
        }
        
        cache.set(cache_key, result)
        return result