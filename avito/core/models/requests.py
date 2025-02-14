# from pydantic import BaseModel, Field, PositiveInt
# from uuid import UUID
#
#
# class BuyMerchRequest(BaseModel):
#     item_name: str = Field(..., description="Название товара для покупки")
#
#
# class TransferCoinsRequest(BaseModel):
#     to_user_id: UUID = Field(..., description="UUID пользователя-получателя")
#     amount: PositiveInt = Field(..., description="Количество монет для перевода")
from pydantic import BaseModel, PositiveInt
from uuid import UUID


class BuyMerchRequest(BaseModel):
    item_name: str


class TransferCoinsRequest(BaseModel):
    to_user_id: UUID
    amount: PositiveInt
