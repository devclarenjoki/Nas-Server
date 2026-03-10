from infrastructure.database import db
from infrastructure.cache import cache
from datetime import datetime
import pytz
from bson import ObjectId

class AdminService:
    
    @staticmethod
    async def get_all_users():
        """Fetches all users from the database."""
        users = list(db.get_collection("users").find({}, {"password": 0})) # Exclude password
        
        results = []
        for user in users:
            results.append({
                "id": str(user["_id"]),
                "email": user.get("email"),
                "role": user.get("role", "user"),
                "created_at": user.get("created_at")
            })
        return results

    @staticmethod
    async def get_all_orders():
        """Fetches all orders across all users."""
        orders = list(db.get_collection("orders").find().sort("created_at", -1))
        
        results = []
        for order in orders:
            results.append({
                "id": str(order["_id"]),
                "user_id": str(order.get("user_id")),
                "type": order.get("type"),
                "status": order.get("status"),
                "region": order.get("region"),
                "fiat_amount": order.get("fiat_amount"),
                "fiat_currency": order.get("fiat_currency"),
                "created_at": order.get("created_at").strftime("%Y-%m-%d %H:%M:%S") if order.get("created_at") else None
            })
        return results

    @staticmethod
    async def update_order_status(order_id: str, status: str):
        """Updates the status of an order."""
        try:
            result = db.get_collection("orders").update_one(
                {"_id": ObjectId(order_id)},
                {"$set": {"status": status, "updated_at": datetime.now(pytz.UTC)}}
            )
            
            if result.matched_count == 0:
                return None
            
            # Clear relevant caches
            # cache.delete(f"orders:{user_id}") # Ideally need user_id here, but can skip for admin update
            
            return {"id": order_id, "status": status}
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def get_dashboard_stats():
        """Aggregates basic stats for the admin dashboard."""
        total_users = db.get_collection("users").count_documents({})
        total_orders = db.get_collection("orders").count_documents({})
        
        return {
            "total_users": total_users,
            "total_orders": total_orders
        }