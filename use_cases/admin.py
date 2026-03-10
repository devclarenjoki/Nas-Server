from domain.admin_services import AdminService
from bson import ObjectId

class AdminUseCase:
    
    @staticmethod
    async def list_all_users():
        users = await AdminService.get_all_users()
        return {"status": "success", "users": users}, 200

    @staticmethod
    async def list_all_orders():
        orders = await AdminService.get_all_orders()
        return {"status": "success", "orders": orders}, 200

    @staticmethod
    async def change_order_status(order_id: str, status: str):
        # Validation
        valid_statuses = ["pending", "processing", "completed", "cancelled"]
        if status not in valid_statuses:
            return {"error": f"Invalid status. Valid values: {valid_statuses}"}, 400
        
        if not ObjectId.is_valid(order_id):
            return {"error": "Invalid Order ID format"}, 400

        result = await AdminService.update_order_status(order_id, status)
        
        if not result:
            return {"error": "Order not found"}, 404
            
        return {"status": "success", "message": "Order updated", "data": result}, 200

    @staticmethod
    async def get_stats():
        stats = await AdminService.get_dashboard_stats()
        return {"status": "success", "stats": stats}, 200