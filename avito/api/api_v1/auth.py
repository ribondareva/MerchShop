from fastapi import APIRouter

from api.api_v1.fastapi_users_router import fastapi_users
from api.dependencies.authentification.backend import authentication_backend
from core.config import settings
from schemas.user import UserRead, UserCreate

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)


# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    ),
)


# /register
router.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)
