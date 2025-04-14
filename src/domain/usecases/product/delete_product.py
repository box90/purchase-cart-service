from src.domain.errors.exceptions import ProductNotFoundError
from src.domain.repositories.product_repository import ProductRepository


class DeleteProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, product_id):
        # Validate the product ID
        if not self.product_repository.get_by_id(product_id):
            raise ProductNotFoundError(f"Invalid product ID {product_id}")

        # Delete the product using the repository
        await self.product_repository.delete(product_id)