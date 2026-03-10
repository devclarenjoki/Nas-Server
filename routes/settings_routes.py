from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from use_cases.settings import SettingsUseCase
from interfaces.dependencies import get_current_user

router = APIRouter(prefix="/settings", tags=["settings"])

# Pydantic model for request validation
class SettingsUpdate(BaseModel):
    theme: str = "light"
    notifications: bool = True

@router.get("/", response_model=dict)
async def get_settings(
    current_user: dict = Depends(get_current_user)
):
    """
    Get user settings
    """
    try:
        result, status = await SettingsUseCase.get_settings(current_user._id)
        if status != 200:
            raise HTTPException(status_code=status, detail=result.get("error"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/")
async def update_settings(
    request_data: SettingsUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update user settings
    """
    try:
        result, status = await SettingsUseCase.update_settings(
            user_id=current_user["_id"],
            theme=request_data.theme,
            notifications=request_data.notifications
        )
        if status != 200:
            raise HTTPException(status_code=status, detail=result.get("error"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))