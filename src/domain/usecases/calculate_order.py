import uuid
from typing import List

from src.domain.dtos.order_request import OrderRequest
from src.domain.models.order import Order
from src.domain.models.product_order import ProductOrder
from src.domain.repositories.product_repository import ProductRepository


class CalculateOrderUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, order_request: OrderRequest) :
        total_price = 0.0
        total_vat = 0.0
        product_list: List[ProductOrder] = []
        for item in order_request.products:
            product = await self.product_repository.get_by_id(item.product_id)
            if product is None:
                raise Exception(f"Product with id {item.product_id} not found")

            total_price += product.price * item.quantity
            total_vat += product.vat * item.quantity
            product_list.append(ProductOrder(
                id=product.id,
                name=product.name,
                quantity=item.quantity,
                price=product.price,
                vat=product.vat,
            ))

        return Order(
            order_id=uuid.uuid4(),
            items=product_list,
            order_price=total_price,
            order_vat=total_vat,
        )