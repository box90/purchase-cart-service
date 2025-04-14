import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.dtos.calculation_request import CalculationRequest
from src.domain.dtos.order_request import OrderRequest
from src.domain.dtos.product_request import ProductRequest
from src.domain.models.order import Order
from src.application.order_service import OrderService
from src.domain.models.product_order import ProductOrder
from src.domain.usecases.calculate_order import CalculateOrderUseCase

@pytest.mark.asyncio
async def test_calculate_order():
    # Arrange
    calculate_order_usecase = AsyncMock(spec=CalculateOrderUseCase)
    order_service = OrderService(calculate_order_usecase=calculate_order_usecase)

    product_order = ProductOrder(1, "Pizza", 10, 2.5,2)

    order_data = OrderRequest(items=[ProductRequest(product_id=1, quantity=2)])
    calculate_data = CalculationRequest(order=order_data.model_dump())

    expected_order = Order(
        order_id=uuid4(),
        items=[product_order],
        order_price=20.0,
        order_vat=4.0,
    )

    calculate_order_usecase.execute.return_value = expected_order

    # Act
    result = await order_service.calculate_order(calculate_data)

    # Assert
    calculate_order_usecase.execute.assert_called_once()
    assert calculate_order_usecase.execute.call_args[0][0].model_dump() == order_data.model_dump()
    assert result == expected_order
