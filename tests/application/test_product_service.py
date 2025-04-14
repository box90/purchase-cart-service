import pytest
from unittest.mock import AsyncMock
from src.application.product_service import ProductService
from src.domain.dtos.upsert_product_request import UpsertProductRequest
from src.domain.models.product import Product

@pytest.mark.asyncio
async def test_get_by_id():
    # Arrange
    get_by_id_usecase = AsyncMock()
    get_by_id_usecase.execute.return_value = Product(1, "Product A", 10.0, 2.0)
    product_service = ProductService(
        list_usecase=AsyncMock(),
        get_by_id_usecase=get_by_id_usecase,
        upsert_usecase=AsyncMock(),
        delete_usecase=AsyncMock(),
    )

    # Act
    result = await product_service.get_by_id(1)

    # Assert
    get_by_id_usecase.execute.assert_called_once_with(1)
    assert result.id == 1
    assert result.name == "Product A"

@pytest.mark.asyncio
async def test_list():
    # Arrange
    list_usecase = AsyncMock()
    list_usecase.execute.return_value = [
        Product(1, "Product A", 10.0, 2.0),
        Product(2, "Product B", 20.0, 4.0),
    ]
    product_service = ProductService(
        list_usecase=list_usecase,
        get_by_id_usecase=AsyncMock(),
        upsert_usecase=AsyncMock(),
        delete_usecase=AsyncMock(),
    )

    # Act
    result = await product_service.list()

    # Assert
    list_usecase.execute.assert_called_once()
    assert len(result) == 2
    assert result[0].name == "Product A"

@pytest.mark.asyncio
async def test_create():
    # Arrange
    get_by_id_usecase = AsyncMock()
    get_by_id_usecase.execute.return_value = None
    upsert_usecase = AsyncMock()
    upsert_usecase.execute.return_value = Product(1, "Product A", 10.0, 2.0)
    product_service = ProductService(
        list_usecase=AsyncMock(),
        get_by_id_usecase=get_by_id_usecase,
        upsert_usecase=upsert_usecase,
        delete_usecase=AsyncMock(),
    )

    # Act
    result = await product_service.create(1, "Product A", 10.0, 2.0)

    # Assert
    get_by_id_usecase.execute.assert_called_once_with(1)
    upsert_usecase.execute.assert_called_once_with(
        UpsertProductRequest(id=1, name="Product A", price=10.0, vat=2.0)
    )
    assert result.name == "Product A"

@pytest.mark.asyncio
async def test_update():
    # Arrange
    get_by_id_usecase = AsyncMock()
    get_by_id_usecase.execute.return_value = Product(1, "Product A", 10.0, 2.0)
    upsert_usecase = AsyncMock()
    upsert_usecase.execute.return_value = Product(1, "Updated Product", 15.0, 3.0)
    product_service = ProductService(
        list_usecase=AsyncMock(),
        get_by_id_usecase=get_by_id_usecase,
        upsert_usecase=upsert_usecase,
        delete_usecase=AsyncMock(),
    )

    # Act
    result = await product_service.update(1, name="Updated Product", price=15.0, vat=3.0)

    # Assert
    get_by_id_usecase.execute.assert_called_once_with(1)
    upsert_usecase.execute.assert_called_once_with(
        UpsertProductRequest(id=1, name="Updated Product", price=15.0, vat=3.0)
    )
    assert result.name == "Updated Product"

@pytest.mark.asyncio
async def test_delete():
    # Arrange
    delete_usecase = AsyncMock()
    delete_usecase.execute.return_value = None
    product_service = ProductService(
        list_usecase=AsyncMock(),
        get_by_id_usecase=AsyncMock(),
        upsert_usecase=AsyncMock(),
        delete_usecase=delete_usecase,
    )

    # Act
    await product_service.delete(1)

    # Assert
    delete_usecase.execute.assert_called_once_with(1)