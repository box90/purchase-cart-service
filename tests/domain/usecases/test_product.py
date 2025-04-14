import pytest
from unittest.mock import AsyncMock

from src.domain.usecases.product.get_product_by_id import GetProductByIdUseCase
from src.domain.usecases.product.delete_product import DeleteProductUseCase
from src.domain.usecases.product.list_products import ListProductsUseCase
from src.domain.dtos.upsert_product_request import UpsertProductRequest
from src.domain.models.product import Product
from src.domain.usecases.product.upsert_product import UpsertProductUseCase


@pytest.mark.asyncio
async def test_get_product_by_id_usecase():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = Product(id=1, name="Product 1", price=10.0, vat=2.0)

    usecase = GetProductByIdUseCase(product_repository=mock_repo)
    product_id = 1

    # Act
    result = await usecase.execute(product_id)

    # Assert
    assert result.id == 1
    assert result.name == "Product 1"
    assert result.price == 10.0
    assert result.vat == 2.0
    mock_repo.get_by_id.assert_called_once_with(product_id)


@pytest.mark.asyncio
async def test_upsert_product_usecase_create():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None  # Simulate that the product does not exist
    mock_repo.create.return_value = Product(id=1, name="New Product", price=10.0, vat=2.0)

    usecase = UpsertProductUseCase(product_repository=mock_repo)
    request = UpsertProductRequest(id=1, name="New Product", price=10.0, vat=2.0)

    # Act
    result = await usecase.execute(request)

    # Assert
    assert result.id == 1
    assert result.name == "New Product"
    assert result.price == 10.0
    assert result.vat == 2.0
    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_upsert_product_usecase_update():
    # Arrange
    existing_product = Product(id=1, name="Existing Product", price=15.0, vat=3.0)
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = existing_product  # Simulate that the product exists
    mock_repo.update.return_value = Product(id=1, name="Updated Product", price=20.0, vat=4.0)

    usecase = UpsertProductUseCase(product_repository=mock_repo)
    request = UpsertProductRequest(id=1, name="Updated Product", price=20.0, vat=4.0)

    # Act
    result = await usecase.execute(request)

    # Assert
    assert result.id == 1
    assert result.name == "Updated Product"
    assert result.price == 20.0
    assert result.vat == 4.0
    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_list_products_usecase():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.list.return_value = [
        Product(id=1, name="Product 1", price=10.0, vat=2.0),
        Product(id=2, name="Product 2", price=20.0, vat=4.0),
    ]  # Simula una lista di prodotti

    usecase = ListProductsUseCase(product_repository=mock_repo)

    # Act
    result = await usecase.execute()

    # Assert
    assert len(result) == 2
    assert result[0].name == "Product 1"
    assert result[1].name == "Product 2"
    mock_repo.list.assert_called_once()


@pytest.mark.asyncio
async def test_delete_product_usecase():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.delete.return_value = None  # Simulate the delete operation

    usecase = DeleteProductUseCase(product_repository=mock_repo)
    product_id = 1

    # Act
    await usecase.execute(product_id)

    # Assert
    mock_repo.delete.assert_called_once_with(product_id)