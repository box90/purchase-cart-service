from contextlib import asynccontextmanager

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.infrastructure.routers.limiter.rate_limiter import limiter
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

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(product_router)
app.include_router(order_router)
