from fastapi import APIRouter

from src.application.dic import DIC
from src.domain.models.product import Product

product_router = APIRouter(
    prefix="/product",
    tags=["Products"],
)

@product_router.get("/", response_model=list[Product])
async def list_products():
    return await DIC.product_service.list()


