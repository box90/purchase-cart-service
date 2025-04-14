import pytest
from src.domain.dtos.order_request import OrderRequest, ProductRequest
from src.domain.models.product import Product
from src.domain.usecases.calculate_order import CalculateOrderUseCase
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_calculate_order_usecase_success():
    # Arrange
    product_id_1 = 1
    product_id_2 = 2

    request = OrderRequest(items=[
        ProductRequest(product_id=product_id_1, quantity=2),
        ProductRequest(product_id=product_id_2, quantity=1)
    ])

    mock_repo = AsyncMock()
    mock_repo.get_by_id.side_effect = [
        Product(id=product_id_1, name="Test Product 1", price=10.0, vat=2.0),
        Product(id=product_id_2, name="Test Product 2", price=20.0, vat=4.0)
    ]

    usecase = CalculateOrderUseCase(product_repository=mock_repo)

    # Act
    result = await usecase.execute(request)

    # Assert
    assert result.order_price == 40.0  # (2*10) + (1*20)
    assert result.order_vat == 8.0  # (2*2) + (1*4)
    assert len(result.items) == 2
    assert result.items[0].name == "Test Product 1"
    assert result.items[1].quantity == 1
    mock_repo.get_by_id.assert_called()


@pytest.mark.asyncio
async def test_calculate_order_product_not_found():
    # Arrange
    fake_id = 1
    request = OrderRequest(items=[ProductRequest(product_id=fake_id, quantity=1)])

    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None

    usecase = CalculateOrderUseCase(product_repository=mock_repo)

    # Act & Assert
    with pytest.raises(Exception) as e:
        await usecase.execute(request)

    assert str(e.value) == f"Product with id {fake_id} not found"
