from pydantic import BaseModel
from typing import List, Optional


class InventoryItem(BaseModel):
    item: str


class TransferCoinsResponse(BaseModel):
    detail: str


class TransactionRecord(BaseModel):
    from_user: str
    to_user: str
    amount: int


class CoinHistory(BaseModel):
    received: List[TransactionRecord]
    sent: List[TransactionRecord]


class InfoResponse(BaseModel):
    coins: int
    inventory: List[InventoryItem]
    coinHistory: CoinHistory
