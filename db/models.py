from datetime import datetime

from typing import Optional, List
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey, DateTime, func
from uuid import UUID


class Base(DeclarativeBase):
    pass


class UserBase(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str] = mapped_column(String(18))

    products: Mapped[List["ProductBase"]] = relationship(
        back_populates="seller", cascade="all, delete-orphan"
    )

    support_chat_sessions: Mapped[List["SupportChatSessionBase"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    messages: Mapped[List["MessageBase"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"UserBase(uuid={self.uuid}, username={self.username})"


class ProductBase(Base):
    __tablename__ = "products"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[float] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    seller: Mapped[UserBase] = relationship(back_populates="products")
    seller_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))

    def __repr__(self) -> str:
        return (f"ProductBase(uuid={self.uuid}, name={self.name}, price={self.price}, "
                f"quantity={self.quantity}")


class SupportChatSessionBase(Base):
    __tablename__ = "support_chat_sessions"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column()
    user: Mapped[Optional[UserBase]] = relationship(back_populates="support_chat_sessions")
    user_uuid: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.uuid"))
    messages: Mapped[list["MessageBase"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class MessageBase(Base):
    __tablename__ = "messages"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user: Mapped[Optional[UserBase]] = relationship(back_populates="messages")
    user_uuid: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.uuid"))

    from_support: Mapped[bool] = mapped_column()

    session: Mapped[SupportChatSessionBase] = relationship(back_populates="messages")
    session_uuid: Mapped[UUID] = mapped_column(ForeignKey("support_chat_sessions.uuid"))

