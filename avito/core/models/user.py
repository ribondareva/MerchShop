from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Integer, default=1000)  # Начальный баланс 1000 монет
    hashed_password = Column(String)
    transactions = relationship("Transaction", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")
