from src.application.dic import DIC
from src.application.order_service import OrderService
from src.application.product_service import ProductService
from src.domain.usecases.calculate_order import CalculateOrderUseCase
from src.domain.usecases.product.delete_product import DeleteProductUseCase
from src.domain.usecases.product.get_product_by_id import GetProductByIdUseCase
from src.domain.usecases.product.list_products import ListProductsUseCase
from src.domain.usecases.product.upsert_product import UpsertProductUseCase
from src.infrastructure.persistence.in_memory_database import InMemoryDatabase
from src.infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository


async def application_startup():
    database = InMemoryDatabase()
    product_repository = InMemoryProductRepository(database)
    calculate_order_usecase = CalculateOrderUseCase(product_repository)
    list_products_usecase = ListProductsUseCase(product_repository)
    get_product_by_id_usecase = GetProductByIdUseCase(product_repository)
    upsert_product_usecase = UpsertProductUseCase(product_repository)
    delete_product_usecase = DeleteProductUseCase(product_repository)

    DIC.order_service = OrderService(
        calculate_order_usecase
    )
    DIC.product_service = ProductService(
        list_usecase=list_products_usecase,
        get_by_id_usecase=get_product_by_id_usecase,
        upsert_usecase=upsert_product_usecase,
        delete_usecase=delete_product_usecase
    )