from fastapi import APIRouter, HTTPException

from src.domain.dtos.product_creation_request import ProductUpsertRequest
from src.domain.errors.exceptions import ProductAlreadyExistsError, ProductNotFoundError
from src.application.dic import DIC
from src.domain.models.product import Product

product_router = APIRouter(
    prefix="/product",
    tags=["Products"],
)

@product_router.get("/", response_model=list[Product])
async def list_products():
    try:
        return await DIC.product_service.list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@product_router.get("/{id}", response_model=Product)
async def get_product(id: int):
    try:
        return await DIC.product_service.get_by_id(id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@product_router.post("/{id}", response_model=Product)
async def create_product(id: int, request: ProductUpsertRequest):
    try:
        return await DIC.product_service.create(id, request.name, request.price, request.vat)
    except ProductAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@product_router.put("/{id}")
async def update_product(id: int, request: ProductUpsertRequest):
    try:
        return await DIC.product_service.update(id, request.name, request.price, request.vat)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@product_router.delete("/{id}")
async def delete_product(id: int):
    try:
        await DIC.product_service.delete(id)
        return {"message": "Product deleted successfully"}
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")