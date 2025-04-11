from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application import application_startup
from src.infrastructure.routers.order import order_router
from src.infrastructure.routers.product import product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await application_startup()
    yield

app = FastAPI(
    title="Cart calculator",
    description="A simple order price calculator made with Python FastAPI",
    lifespan=lifespan
)

app.include_router(product_router)
app.include_router(order_router)
