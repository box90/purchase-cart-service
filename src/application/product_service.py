from src.domain.errors.exceptions import ProductAlreadyExistsError, ProductNotFoundError
from src.domain.dtos.upsert_product_request import UpsertProductRequest
from src.domain.models.product import Product
from src.domain.usecases.product.delete_product import DeleteProductUseCase
from src.domain.usecases.product.get_product_by_id import GetProductByIdUseCase
from src.domain.usecases.product.list_products import ListProductsUseCase
from src.domain.usecases.product.upsert_product import UpsertProductUseCase


class ProductService:
    def __init__(
            self,
            list_usecase: ListProductsUseCase,
            get_by_id_usecase: GetProductByIdUseCase,
            upsert_usecase: UpsertProductUseCase,
            delete_usecase: DeleteProductUseCase
        ):
        self.list_usecase = list_usecase
        self.get_by_id_usecase = get_by_id_usecase
        self.upsert_usecase = upsert_usecase
        self.delete_usecase = delete_usecase

    async def get_by_id(self, id: int) -> Product | None:
        return await self.get_by_id_usecase.execute(id)

    async def list(self) -> list[Product]:
        return await self.list_usecase.execute()

    async def create(self, id: int, name: str, price: float, vat: float) -> Product:
        if await self.get_by_id_usecase.execute(id):
            raise ProductAlreadyExistsError(f"Product already exists with id {id}")
        item = UpsertProductRequest(id=id, name=name, price=price, vat=vat)
        return await self.upsert_usecase.execute(item)

    async def update(self, id: int, name: str = None, price: float = None, vat: float = None) -> Product:
        if not await self.get_by_id_usecase.execute(id):
            raise ProductNotFoundError("Product not found")
        item = UpsertProductRequest(id=id, name=name, price=price, vat=vat)
        return await self.upsert_usecase.execute(item)

    async def delete(self, id: int):
        return await self.delete_usecase.execute(id)
