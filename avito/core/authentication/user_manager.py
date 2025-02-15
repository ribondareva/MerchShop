import logging
import uuid
from typing import Optional, TYPE_CHECKING
from fastapi_users import BaseUserManager, UUIDIDMixin
from sqlalchemy import select

from core.config import settings
from core.models import User, db_helper
from passlib.context import CryptContext
from fastapi import Request, HTTPException

log = logging.getLogger(__name__)

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    def __init__(self, user_db):
        super().__init__(user_db)
        self.pwd_context = pwd_context

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token %r",
            user.id,
            token,
        )

    async def get_by_username(self, username: str) -> User:
        async for session in db_helper.session_getter():
            user = await session.execute(select(User).filter(User.username == username))
            user = user.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        # Проверяем пароль с использованием Argon2id
        return self.pwd_context.verify(password, hashed_password)
