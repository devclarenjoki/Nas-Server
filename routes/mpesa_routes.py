from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from use_cases.mpesa import MpesaUseCase
from interfaces.dependencies import get_current_admin_user

router = APIRouter(prefix="/api/mpesa", tags=["M-Pesa"])

class StkPushRequest(BaseModel):
    phone: str
    amount: float
    account: str = "EXAMPLE" # Optional account reference

@router.post("/stk", status_code=status.HTTP_200_OK)
async def stk_push_endpoint(
    data: StkPushRequest,
    current_user: dict = Depends(get_current_admin_user) # Protected route
):
    """
    Initiate M-Pesa STK Push.

    """
    result, status_code = await MpesaUseCase.stk_push(
        phone=data.phone,
        amount=data.amount,
        account_reference=data.account
    )
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result.get("error"))
        
    return result