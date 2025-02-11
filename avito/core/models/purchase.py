from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class Purchase(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    merch_item_id = Column(Integer, ForeignKey("merch_items.id"), nullable=False)

    user = relationship("User", back_populates="purchases")
    merch_item = relationship("MerchItem", backref="purchases")
