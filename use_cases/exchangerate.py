from domain.exchange_services import ExchangeRateService

class ExchangeRateUseCase:
    
    @staticmethod
    async def update_rates():
        """Orchestrates the fetching and storing of rates"""
        data = await ExchangeRateService.fetch_and_store_rates()
        
        if not data:
            return {"error": "Failed to fetch or store exchange rates"}, 500
            
        return {
            "status": "success", 
            "message": "Exchange rates updated successfully",
            "data": data
        }, 201

    @staticmethod
    async def get_current_rates():
        """Gets the latest rates available in the system"""
        data = await ExchangeRateService.get_latest_rates()
        
        if not data:
            return {"error": "No exchange rate data found"}, 404
            
        return {"status": "success", "data": data}, 200