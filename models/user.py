from uuid import UUID

from pydantic import BaseModel

from models.products import Product


class User(BaseModel):
    uuid: UUID
    username: str


class UserWithPassword(User):
    hashed_password: str


class Seller(User):
    products: list[Product]
