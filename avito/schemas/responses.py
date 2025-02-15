from pydantic import BaseModel, Field
from typing import List, Optional


class InventoryItem(BaseModel):
    item: str


class TransferCoinsResponse(BaseModel):
    detail: str


class TransactionRecord(BaseModel):
    from_user: Optional[str] = None
    to_user: Optional[str] = None
    amount: int


class CoinHistory(BaseModel):
    received: List[TransactionRecord]
    sent: List[TransactionRecord]


class InfoResponse(BaseModel):
    coins: int
    inventory: List[InventoryItem]
    coinHistory: CoinHistory


class ErrorResponse(BaseModel):
    errors: str = Field(..., description="Сообщение об ошибке, описывающее проблему.")

    class Config:
        json_schema_extra = {"example": {"errors": "Произошла ошибка."}}
