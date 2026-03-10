from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from use_cases.auth import AuthUseCase
from interfaces.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

# Pydantic models for request validation
class RegisterRequest(BaseModel):
    name: str
    phone: str
    country: str
    pin: str

class LoginRequest(BaseModel):
    phone:str
    pin: str

@router.post("/register", status_code=201)
async def register(request_data: RegisterRequest):
    """
    Register a new user
    """
    # # Validate passwords match
    # if request_data.password != request_data.confirmpassword:
    #     raise HTTPException(status_code=400, detail="Passwords do not match")
    
    try:
        result, status = await AuthUseCase.register(
            name=request_data.name,
            phone=request_data.phone,
            country=request_data.country,
            pin=request_data.pin,
            isAdmin="false"
        )
        if status != 201:
            raise HTTPException(status_code=status, detail=result.get("error"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(
    request_data: LoginRequest,
    response: Response
):
    """
    Login user and set session cookie
    """
    try:
        result, status = await AuthUseCase.login(
            phone=request_data.phone,
            pin=request_data.pin
        )
        
        if status == 200:
            response.set_cookie(
                key="session_token",
                value=result["access_token"],
                httponly=True,
                secure=True,  # Set to False for HTTP development
                samesite="strict",
                max_age=result["expires_in"],
                expires=result["expires_in"]
            )
            return {"message": "Login successful", "user": result}
        else:
            raise HTTPException(status_code=status, detail=result.get("error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logout")
async def logout(
    response: Response,
    current_user: dict = Depends(get_current_user)
):
    """
    Logout user and delete session cookie
    """
    response.delete_cookie(
        key="session_token",
        httponly=True,
        secure=True,
        samesite="strict"
    )
    return {"message": "Logout successful"}