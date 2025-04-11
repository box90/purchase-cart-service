from fastapi import APIRouter

from src.application.dic import DIC
from src.domain.dtos.order_request import OrderRequest
from src.domain.models.order import Order

order_router = APIRouter(
    prefix="/order",
    tags=["Order"],
)

@order_router.post("/calculate", response_model=Order)
async def calculate_order(request: OrderRequest):
    return await DIC.order_service.calculate_order(request)