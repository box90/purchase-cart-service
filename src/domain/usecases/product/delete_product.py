from src.domain.repositories.product_repository import ProductRepository


class DeleteProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, product_id):
        # Validate the product ID
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("Invalid product ID")

        # Delete the product using the repository
        await self.product_repository.delete(product_id)