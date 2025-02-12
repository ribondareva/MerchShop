from pydantic import BaseModel, ConfigDict
from uuid import UUID


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    hashed_password: str


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
