from infrastructure.database import db
from infrastructure.cache import cache
from datetime import datetime, timedelta
import pytz
import uuid

class OrderService:
    @staticmethod
    async def create_onramp_order(user_id, order_data):
        """
        Creates an order.
        Handles reference ID generation, fee calculation, and rate locking 
        (as per Next.js route comments).
        """
        # Extract data
        order_type = order_data.get('type')
        region = order_data.get('region')
        
        # 1. Rate Locking & Fee Calculation Logic (Mock implementation)
        # In a real scenario, you would fetch current rates from an external service
        # calculated_fee = 10.00 # Mock fee
        # locked_rate = 1.05 # Mock rate

        created_at=datetime.now(pytz.UTC)
        expires_at = created_at + timedelta(minutes=15) # 15 minutes expiry
        reference = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        document = {
            "user_id": user_id,
            "type": order_type,
            "region": region,
            "status": "pending",
            "fiat_amount": order_data.get('fiatAmount'),
            "fiat_currency": order_data.get('fiatCurrency'),
            "wallet_address": order_data.get('walletAddress'),
            "reference_id":reference,
            "fee": order_data.get('fee'),
            "rate": order_data.get('fxRate'),
            "created_at": created_at,
            "expires_at": expires_at


        }
        
        # Insert into DB
        result = db.get_collection("orders").insert_one(document)
        
        # Invalidate cache for user orders
        cache.delete(f"orders:{user_id}")
        
        # Return the created object (including the generated ID)
        document["_id"] = result.inserted_id
        return {
            "user_id": str(user_id),
            "type": document["type"],
            "region": document["region"],
            "fiatAmount": document["fiat_amount"],
            "fiatCurrency": document["fiat_currency"],
            "walletAddress": document["wallet_address"],
            "status": document["status"],
            "reference_id":document["reference_id"],
            "fee": document["fee"],
            "created_at": created_at.isoformat(),
            "expires_at": expires_at.isoformat()
        }

    @staticmethod
    async def create_offramp_order(user_id, order_data):
        """
        Creates an order.
        Handles reference ID generation, fee calculation, and rate locking 
        (as per Next.js route comments).
        """
        # Extract data
        order_type = order_data.get('type')
        region = order_data.get('region')
        
        # 1. Rate Locking & Fee Calculation Logic (Mock implementation)
        # In a real scenario, you would fetch current rates from an external service
        calculated_fee = 10.00 # Mock fee
        locked_rate = 1.05 # Mock rate

        created_at=datetime.now(pytz.UTC)
        expires_at = created_at + timedelta(minutes=15) # 15 minutes expiry
        reference = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        document = {
            "user_id": user_id,
            "type": order_type,
            "region": region,
            "status": "pending",
            "usdt_amount": order_data.get('usdtAmount'),
            "reference_id":reference,
            "fee": calculated_fee,
            "rate": locked_rate,
            "created_at": created_at,
            "expires_at": expires_at


        }
        
        # Insert into DB
        result = db.get_collection("orders").insert_one(document)
        
        # Invalidate cache for user orders
        cache.delete(f"orders:{user_id}")
        
        # Return the created object (including the generated ID)
        document["_id"] = result.inserted_id
        return {
            "user_id": str(user_id),
            "type": document["type"],
            "region": document["region"],
            "usdtAmount": document["usdt_amount"],
            "status": document["status"],
            "reference_id":document["reference_id"],
            "fee": document["fee"],
            "created_at": created_at.isoformat(),
            "expires_at": expires_at.isoformat()
        }

    @staticmethod
    async def get_orders(user_id):
        """Fetch all orders for a specific user"""
        # Check cache
        cache_key = f"orders:{user_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Fetch from DB
        documents = list(db.get_collection("orders")
                        .find({"user_id": user_id})
                        .sort("created_at", -1))
        
        # Format results
        results = []
        for doc in documents:
            results.append({
                "id": str(doc["_id"]),
                "type": doc["type"],
                "region": doc["region"],
                "status": doc["status"],
                "fiatAmount": doc.get("fiat_amount"),
                "fiatCurrency": doc.get("fiat_currency"),
                "walletAddress": doc.get("wallet_address"),
                "fee": doc.get("fee"),
                "created_at": doc["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
                "expires_at": doc["expires_at"].strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Set cache
        cache.set(cache_key, results)
        return results