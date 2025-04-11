from src.domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self):
        return await self.product_repository.list()