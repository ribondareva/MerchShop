import uuid
from typing import Optional

from pydantic import ConfigDict
from pydantic import EmailStr
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: Optional[EmailStr]


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
    email: Optional[EmailStr]
