from pydantic import BaseModel

from src.domain.dtos.order_request import OrderRequest


class CalculationRequest(BaseModel):
    order: OrderRequest