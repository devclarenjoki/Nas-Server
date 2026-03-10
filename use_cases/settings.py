from domain.services import SettingsService

class SettingsUseCase:
    @staticmethod
    async def get_settings(user_id):
        settings = await SettingsService.get_settings(user_id)
        if settings:
            return {"settings": settings}, 200
        return {"error": "Settings not found"}, 404
    
    @staticmethod
    async def update_settings(user_id, theme=None, notifications=None):
        success = await SettingsService.update_settings(user_id, theme, notifications)
        if success:
            return {"message": "Settings updated successfully"}, 200
        return {"error": "No valid fields to update or settings not found"}, 400
