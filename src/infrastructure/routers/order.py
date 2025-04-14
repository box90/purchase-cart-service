from fastapi import APIRouter, HTTPException

from src.domain.dtos.calculation_request import CalculationRequest
from src.domain.errors.exceptions import OrderValidationError
from src.application.dic import DIC
from src.domain.models.order import Order

order_router = APIRouter(
    prefix="/order",
    tags=["Order"],
)

@order_router.post("/calculate", response_model=Order)
async def calculate_order(request: CalculationRequest):
    try:
        return await DIC.order_service.calculate_order(request)
    except OrderValidationError:
        raise HTTPException(status_code=400, detail="Invalid order data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")