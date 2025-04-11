from dataclasses import dataclass

from src.domain.models.product import Product

@dataclass
class ProductOrder(Product):
    quantity: int

