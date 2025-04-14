from pydantic import BaseModel


class ProductUpsertRequest(BaseModel):
    name: str
    price: float
    vat: float