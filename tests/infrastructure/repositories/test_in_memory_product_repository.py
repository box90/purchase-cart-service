import pytest
from unittest.mock import MagicMock
from src.domain.models.product import Product
from src.infrastructure.persistence.in_memory_database import InMemoryDatabase
from src.infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository

@pytest.mark.asyncio
async def test_add_product_and_get_by_id():
    # Arrange
    db = InMemoryDatabase(True)
    product_id = 1
    product = Product(id=product_id, name="Pizza", price=12.0, vat=2.5)

    repo = InMemoryProductRepository(db)

    # Act
    await repo.create(product)
    result = await repo.get_by_id(product_id)

    # Assert
    assert result is not None
    assert result.id == product_id
    assert result.name == "Pizza"


@pytest.mark.asyncio
async def test_get_by_id_returns_none_if_not_found():
    db = InMemoryDatabase(True)

    repo = InMemoryProductRepository(db)

    result = await repo.get_by_id(123)

    assert result is None


@pytest.mark.asyncio
async def test_delete_product():
    # Arrange
    db = InMemoryDatabase(True)
    product_id = 1
    product = Product(id=product_id, name="Pizza", price=12.0, vat=2.5)

    repo = InMemoryProductRepository(db)

    # Act
    await repo.create(product)
    await repo.delete(product_id)
    result = await repo.get_by_id(product_id)

    # Assert
    assert result is None
