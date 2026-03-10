from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from use_cases.order import OrderUseCase
from interfaces.dependencies import get_current_user

router = APIRouter(prefix="/api/orders", tags=["orders"])

# Pydantic Models
class OrderOnrampCreateRequest(BaseModel):
    type: str
    region: str
    fiatAmount: float
    fiatCurrency: str
    fee: float
    fxRate:float
    walletAddress:str

class OrderOfframpCreateRequest(BaseModel):
    type: str
    region: str
    usdtAmount: float
    fee: float
    fxRate:float

# POST - Create new onramp order
@router.post("/onramp/new", status_code=status.HTTP_201_CREATED)
async def create_onramp_order(
    data: OrderOnrampCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new order (matches Next.js POST functionality)"""
    # UseCase handles validation and logic
    result, status_code = await OrderUseCase.create_onramp_order(
        current_user._id, 
        data.dict()
    )
    
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=result.get("error"))
    
    return result


# POST - Create new offramp order
@router.post("/offramp/new", status_code=status.HTTP_201_CREATED)
async def create_offramp_order(
    data: OrderOfframpCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new order (matches Next.js POST functionality)"""
    # UseCase handles validation and logic
    result, status_code = await OrderUseCase.create_offramp_order(
        current_user._id, 
        data.dict()
    )
    
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=result.get("error"))
    
    return result


# GET - Fetch user's orders
@router.get("")
async def get_orders(
    current_user: dict = Depends(get_current_user)
):
    """Fetch user's orders (matches Next.js GET functionality)"""
    result, status_code = await OrderUseCase.get_orders(current_user._id)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result.get("error"))
    
    return result