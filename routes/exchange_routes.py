from fastapi import APIRouter, Depends, HTTPException, status
from use_cases.exchangerate import ExchangeRateUseCase
from interfaces.dependencies import get_current_user

router = APIRouter(prefix="/api/exchange-rates", tags=["Exchange Rates"])

@router.post("/update", status_code=status.HTTP_201_CREATED)
async def update_exchange_rates(
    current_user: dict = Depends(get_current_user)
):
    """
    Trigger a manual update of exchange rates from the external API.
    Typically an admin or system trigger.
    """
    result, status_code = await ExchangeRateUseCase.update_rates()
    
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=result.get("error"))
    
    return result

@router.get("/latest")
async def get_latest_exchange_rates(
    current_user: dict = Depends(get_current_user)
):
    """
    Get the latest stored exchange rates.
    """
    result, status_code = await ExchangeRateUseCase.get_current_rates()
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result.get("error"))
    
    return result