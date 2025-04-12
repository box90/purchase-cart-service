from dataclasses import dataclass, field

@dataclass
class InMemoryDatabase:
    """
    A simple in-memory database class that can be used to store and retrieve data.
    """

    products: dict = field(default_factory=dict)

    def __init__(self,empty: bool = False):
        self.products = {} if empty else {
            1: {"id": 1, "name": "Product 1", "price": 10.0, "vat": 0.2},
            2: {"id": 2, "name": "Product 2", "price": 20.0, "vat": 0.5},
            3: {"id": 3, "name": "Product 3", "price": 30.0, "vat": 1.0},
        }

