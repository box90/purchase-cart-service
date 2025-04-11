from abc import ABC, abstractmethod
from typing import List

from src.domain.models.product import Product


class ProductRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: int) -> Product | None: ...

    @abstractmethod
    async def list(self) -> List[Product]: ...

    @abstractmethod
    async def create(self, item: Product) -> Product : ...

    @abstractmethod
    async def update(self, item: Product) -> Product : ...

    @abstractmethod
    async def delete(self, id: int) -> None: ...