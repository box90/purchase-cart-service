from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.domain.models.product_order import ProductOrder


@dataclass
class Order:
    """
    Order model class.
    """
    order_id: UUID
    items: List[ProductOrder]
    order_price: float
    order_vat: float
