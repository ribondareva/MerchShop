from pydantic import BaseModel, PositiveInt
from uuid import UUID


class BuyMerchRequest(BaseModel):
    item_name: str


class TransferCoinsRequest(BaseModel):
    to_user_id: UUID
    amount: PositiveInt
