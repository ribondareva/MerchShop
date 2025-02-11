from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base
from sqlalchemy import Index
from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True)
    balance = Column(BigInteger, default=1000)  # Начальный баланс 1000 монет
    hashed_password = Column(String(128))
    transactions = relationship(
        "Transaction", back_populates="user", foreign_keys="[Transaction.from_user_id]"
    )
    purchases = relationship("Purchase", back_populates="user")
    __table_args__ = (
        Index("idx_users_username", "username"),
    )  # Индекс для быстрого поиска
