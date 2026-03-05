from uuid import UUID
from pydantic import BaseModel


class Product(BaseModel):
    uuid: UUID
    name: str
    price: float
    quantity: int
    seller_username: str
    seller_uuid: UUID


class ProductInCart(Product):
    quantity_in_cart: int = 0
    total_price: float = 0