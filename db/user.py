from uuid import uuid4, UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.main import commit_after, set_session
from db.models import UserBase
from models.user import User, UserWithPassword


@commit_after
async def create_user(session: Session, username: str, hashed_password: str) -> None:
    session.add(UserBase(
        uuid=uuid4(),
        username=username,
        hashed_password=hashed_password
    ))


@set_session
async def get_user_by_uuid(session: Session, uuid: UUID, with_password: bool = False) -> User | UserWithPassword | None:
    statement = select(UserBase).where(UserBase.uuid == uuid)
    user = session.scalars(statement).one_or_none()

    if user:
        if with_password:
            return UserWithPassword(uuid=user.uuid, username=user.username, hashed_password=user.hashed_password)
        else:
            return User(uuid=user.uuid, username=user.username)

    return None


@set_session
async def get_user(session: Session, username: str, with_password: bool = False) -> User | UserWithPassword | None:
    statement = select(UserBase).where(UserBase.username == username)
    user = session.scalars(statement).one_or_none()

    if user:
        if with_password:
            return UserWithPassword(uuid=user.uuid, username=user.username, hashed_password=user.hashed_password)
        else:
            return User(uuid=user.uuid, username=user.username)

    return None