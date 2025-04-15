from fastapi import APIRouter, HTTPException, Request

from src.infrastructure.routers.limiter.rate_limiter import limiter
from src.domain.dtos.calculation_request import CalculationRequest
from src.domain.errors.exceptions import OrderValidationError
from src.application.dic import DIC
from src.domain.models.order import Order

order_router = APIRouter(
    prefix="/order",
    tags=["Order"],
)

@order_router.post("/calculate", response_model=Order)
@limiter.limit("5/minute")
async def calculate_order(request: Request, calculation_request: CalculationRequest):
    try:
        return await DIC.order_service.calculate_order(calculation_request)
    except OrderValidationError:
        raise HTTPException(status_code=400, detail="Invalid order data")