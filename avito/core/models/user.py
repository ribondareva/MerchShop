from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy.dialects.postgresql import UUID

from .base import Base
from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy.orm import relationship
from uuid import uuid4

from ..types.user_id import UserIDType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(
    Base,
    SQLAlchemyBaseUserTable[UserIDType],
):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    username = Column(String(50), unique=True, nullable=False)
    balance = Column(
        BigInteger, nullable=False, server_default="1000"
    )  # Начальный баланс 1000 монет
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    sent_transactions = relationship(
        "Transaction",
        back_populates="sender",
        foreign_keys="[Transaction.sender_id]",
    )
    received_transactions = relationship(
        "Transaction",
        back_populates="receiver",
        foreign_keys="[Transaction.receiver_id]",
    )
    purchases = relationship("Purchase", back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
