from sqlalchemy.orm import relationship

from .base import Base
from sqlalchemy import Column, Integer, String


class MerchItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    purchases = relationship("Purchase", back_populates="merch_item")

