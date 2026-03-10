from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from use_cases.user import UserUseCase
from interfaces.dependencies import get_current_user  # We'll create this dependency

router = APIRouter()

@router.get("/profile", response_model=dict)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user's profile
    """
    try:
        
        # Assuming UserUseCase.get_profile is now async
        result, status = await UserUseCase.get_profile(current_user._id)
        return JSONResponse(content=result, status_code=status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
