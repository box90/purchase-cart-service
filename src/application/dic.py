from dataclasses import dataclass

from src.application.order_service import OrderService
from src.application.product_service import ProductService


@dataclass
class DependencyInjectionContainer:
    """
    Dependency Injection Container class.
    """
    order_service: OrderService | None = None
    product_service: ProductService | None = None


DIC = DependencyInjectionContainer()