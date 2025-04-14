from src.domain.dtos.calculation_request import CalculationRequest
from src.domain.models.order import Order
from src.domain.usecases.calculate_order import CalculateOrderUseCase


class OrderService:
    def __init__(self, calculate_order_usecase: CalculateOrderUseCase):
        self.calculate_order_usecase = calculate_order_usecase

    async def calculate_order(self, calculation_data: CalculationRequest) -> Order:
        """
        Calculate the order based on the provided order data.

        :param calculation_data: The order data containing product IDs and quantities.
        :return: An Order object containing the calculated order details.
        """
        return await self.calculate_order_usecase.execute(calculation_data.order)