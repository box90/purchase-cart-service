from pydantic import BaseModel

from src.domain.dtos.product_request import ProductRequest


class OrderRequest(BaseModel):
    products: list[ProductRequest]