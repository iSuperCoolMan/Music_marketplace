from uuid import uuid4, UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.main import commit_after, set_session
from db.models import UserBase, ProductBase
from models.products import Product
from models.user import User


@commit_after
async def create_product(session: Session, name: str, price: float, quantity: int, seller_uuid: UUID) -> None:
    statement = select(UserBase).where(UserBase.uuid == seller_uuid)
    seller = session.scalars(statement).one_or_none()

    if seller is None:
        raise ValueError

    session.add(ProductBase(
        uuid=uuid4(),
        name=name,
        price=price,
        quantity=quantity,
        seller=seller,
        seller_uuid=seller_uuid
    ))


@set_session
async def get_all_products(session: Session) -> list[Product]:
    statement = select(ProductBase)
    products = session.scalars(statement).all()

    return [Product(
        uuid=product.uuid,
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        seller_username=product.seller.username,
        seller_uuid=product.seller.uuid
    ) for product in products]


@set_session
async def get_products_by_uuids(session: Session, uuids: list[UUID]):
    statement = select(ProductBase).filter(ProductBase.uuid.in_(uuids))
    products = session.execute(statement).scalars().all()

    return [Product(
        uuid=product.uuid,
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        seller_username=product.seller.username,
        seller_uuid=product.seller.uuid
    ) for product in products]


@set_session
async def get_products_by_user(session: Session, user_uuid: UUID) -> list[Product]:
    statement = select(ProductBase).where(ProductBase.seller_uuid == user_uuid)
    products = session.scalars(statement).all()

    return [Product(
        uuid=product.uuid,
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        seller_username=product.seller.username,
        seller_uuid=product.seller.uuid
    ) for product in products]