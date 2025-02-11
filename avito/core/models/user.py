from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base
from sqlalchemy import Column, String, BigInteger, text
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    username = Column(String(50), unique=True, nullable=False, index=True)
    balance = Column(BigInteger, nullable=False, default=1000)  # Начальный баланс 1000 монет
    hashed_password = Column(String(128), nullable=False)
    sent_transactions = relationship("Transaction", foreign_keys="[Transaction.from_user_id]")
    received_transactions = relationship("Transaction", foreign_keys="[Transaction.to_user_id]")
    purchases = relationship("Purchase", back_populates="user")
