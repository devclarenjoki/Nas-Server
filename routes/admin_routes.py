from fastapi import APIRouter, Depends, HTTPException, status, Body,BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional
from use_cases.admin import AdminUseCase
from interfaces.dependencies import get_current_user,get_current_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"])

# --- Pydantic Models ---

class OrderStatusUpdate(BaseModel):
    status: str

# --- Dependencies ---


# --- Routes ---

@router.get("/stats", dependencies=[Depends(get_current_admin_user)])
async def get_dashboard_stats():
    """Get dashboard statistics."""
    result, status_code = await AdminUseCase.get_stats()
    return result

@router.get("/users", dependencies=[Depends(get_current_admin_user)])
async def list_users():
    """Get a list of all users."""
    result, status_code = await AdminUseCase.list_all_users()
    return result

@router.get("/orders", dependencies=[Depends(get_current_admin_user)])
async def list_all_orders():
    """Get a list of all orders system-wide."""
    result, status_code = await AdminUseCase.list_all_orders()
    return result

@router.patch("/orders/{order_id}", dependencies=[Depends(get_current_admin_user)])
async def update_order_status(
    order_id: str,
    background_tasks: BackgroundTasks,
    body: OrderStatusUpdate
):
    """Update the status of a specific order."""
    result, status_code = await AdminUseCase.change_order_status(order_id, body.status)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result.get("error"))

    
    # 2. Trigger Background Task if necessary
    # We trigger this if the admin sets it to PROCESSING to ensure the subsequent steps (Transfer/Complete) happen.
    if body.status == "PROCESSING":
        # Fetch order data needed for the background task
        order = db.get_collection("orders").find_one({"_id": ObjectId(order_id)})
        
        if order:
            # Import the service
            from domain.order_processor_service import OrderProcessorService
            
            # Prepare data payload
            order_data = {
                "walletAddress": order.get("wallet_address"),
                "amount": order.get("fiat_amount") # Or calculated crypto amount
            }
            
            # Add task to background
            background_tasks.add_task(
                OrderProcessorService.start_order_lifecycle, 
                order_id,
                order_data
            )
    
    return result