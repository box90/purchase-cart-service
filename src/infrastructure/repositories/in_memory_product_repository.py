from typing import List

from src.domain.models.product import Product
from src.domain.repositories.product_repository import ProductRepository
from src.infrastructure.persistence.in_memory_database import InMemoryDatabase


async def _build_product_model(item: dict) -> Product:
    return Product(
        id=item["id"],
        name=item["name"],
        price=item["price"],
        vat=item["vat"]
    )

async def _serialize_product_to_dict(item: Product) -> dict:
    return {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "vat": item.vat
    }


class InMemoryProductRepository(ProductRepository):

    def __init__(self, database: InMemoryDatabase):
        self.database = database

    async def get_by_id(self, id: int) -> Product | None:
        if id not in self.database.products:
            return None
        return await _build_product_model(self.database.products[id])

    async def list(self) -> List[Product]:
        return [await _build_product_model(product) for _, product in self.database.products.items()]

    async def create(self, item: Product) -> Product:
        product_dict = await _serialize_product_to_dict(item)
        if item.id in self.database.products:
            raise Exception(f"Product already exists with id {item.id}")
        self.database.products[item.id] = product_dict
        return await _build_product_model(product_dict)

    async def update(self, item: Product) -> Product:
        product_data = await _serialize_product_to_dict(item)
        if item.id not in self.database.products:
            raise Exception("Product not found")
        self.database.products[item.id] = product_data
        return await _build_product_model(product_data)


    async def delete(self, id: int) -> None:
        if id in self.database.products:
            del self.database.products[id]

