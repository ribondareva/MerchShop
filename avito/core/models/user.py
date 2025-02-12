from sqlalchemy.dialects.postgresql import UUID

from .base import Base
from sqlalchemy import Column, String, BigInteger, text
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    username = Column(String(50), unique=True, nullable=False)
    balance = Column(BigInteger, nullable=False, server_default="1000")  # Начальный баланс 1000 монет
    hashed_password = Column(String(128), nullable=False)
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
