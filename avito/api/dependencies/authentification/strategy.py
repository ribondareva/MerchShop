from fastapi_users.authentication.strategy.jwt import JWTStrategy
from core.config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.jwt_secret_key,
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )
