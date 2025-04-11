from src.domain.dtos.upsert_product_request import UpsertProductRequest
from src.domain.models.product import Product
from src.domain.repositories.product_repository import ProductRepository


class UpsertProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, request: UpsertProductRequest) -> Product:
        if not self.product_repository.get_by_id(request.id):
            # If the product does not exist, insert it
            return await self.product_repository.create(Product(
                id=request.id,
                name=request.name,
                price=request.price,
                vat=request.vat,
            ))

        await self.product_repository.update(Product(
                id=request.id,
                name=request.name,
                price=request.price,
                vat=request.vat,
            ))