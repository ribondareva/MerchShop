from pydantic import BaseModel, UUID4, ConfigDict
from datetime import datetime


class TransactionResponse(BaseModel):
    id: int
    sender_id: UUID4
    receiver_id: UUID4
    amount: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            sender_id=str(obj.sender_id),
            receiver_id=str(obj.receiver_id),
            amount=obj.amount,
            timestamp=obj.timestamp,
        )
