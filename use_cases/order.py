from domain.order_services import OrderService

class OrderUseCase:
    @staticmethod
    async def create_onramp_order(user_id, data):
        # Basic validation (matching Next.js route)
        required_fields = ['type', 'region', 'fiatCurrency', 'fiatAmount', 'walletAddress']
        
        # Validate fields
        if not all(field in data for field in required_fields):
            return {"error": "Missing required fields"}, 400
        
        if not data['type'] or not data['region']:
             return {"error": "Missing required fields"}, 400

        # Call service to handle logic
        order = await OrderService.create_onramp_order(user_id, data)
        
        # Return success response
        return {
            "status": "success",
            "message": "Order created successfully",
            "order": order
        }, 201

    @staticmethod
    async def create_offramp_order(user_id, data):
        # Basic validation (matching Next.js route)
        required_fields = ['type', 'region', 'fee', 'fxRate','usdtAmount']
        
        # Validate fields
        if not all(field in data for field in required_fields):
            return {"error": "Missing required fields"}, 400
        
        if not data['type'] or not data['region']:
             return {"error": "Missing required fields"}, 400

        # Call service to handle logic
        order = await OrderService.create_offramp_order(user_id, data)
        
        # Return success response
        return {
            "status": "success",
            "message": "Order created successfully",
            "order": order
        }, 201

    @staticmethod
    async def get_orders(user_id):
        orders = await OrderService.get_orders(user_id)
        return {"orders": orders}, 200