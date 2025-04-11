from pydantic import BaseModel


class UpsertProductRequest(BaseModel):
    id: int
    name: str | None
    price: float | None
    vat: float | None