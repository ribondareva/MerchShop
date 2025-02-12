from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from .base import Base


class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship(
        "User", foreign_keys=[sender_id], back_populates="sent_transactions",
    )
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_transactions",
    )
    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
        Index('ix_sender_id', 'sender_id'),
        Index('ix_receiver_id', 'receiver_id'),
    )
