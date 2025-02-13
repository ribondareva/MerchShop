import logging
import uuid
from typing import Optional, TYPE_CHECKING
from fastapi_users import BaseUserManager, UUIDIDMixin
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User, db_helper
from schemas.user import UserCreate


if TYPE_CHECKING:
    from fastapi import Request


log = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
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

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional["Request"] = None,
    ) -> User:
        # Не проверяем email, только username
        await self.validate_username(
            user_create.username
        )  # Проверка уникальности username
        return await super().create(user_create, safe, request)

    # Убираем работу с email
    async def validate_username(self, username: str):
        user = await self.get_by_username(username)
        if user:
            raise ValueError("Username already taken")

    @staticmethod
    async def get_by_username(username: str) -> User | None:
        query = await db_helper.session_factory().execute(
            select(User).where(User.username == username)
        )
        result = query.scalar_one_or_none()
        return result
