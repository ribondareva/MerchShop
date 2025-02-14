from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.api_v1.fastapi_users_router import fastapi_users
from api.dependencies.authentification.backend import authentication_backend
from core.config import settings
from schemas.user import UserRead, UserCreate

from fastapi import Depends, HTTPException, Request

# from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

# from api.api_v1.fastapi_users_router import fastapi_users
from fastapi_users.exceptions import InvalidPasswordException, UserNotExists


router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)


# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        # requires_verification=True
    ),
    responses={
        200: {"description": "Успешная аутентификация."},
        400: {"description": "Неверный запрос."},
    },
    default_response_class=JSONResponse,
)


# @router.post(
#     "/login",
#     summary="Аутентификация и получение JWT-токена.",
#     responses={
#         200: {
#             "description": "Успешная аутентификация.",
#             "content": {
#                 "application/json": {
#                     "example": {
#                         "access_token": "jwt_token_example",
#                         "token_type": "bearer",
#                     }
#                 }
#             },
#         },
#         400: {
#             "description": "Неверный запрос.",
#             "content": {
#                 "application/json": {
#                     "example": {"detail": "Некорректные учетные данные"}
#                 }
#             },
#         },
#         401: {
#             "description": "Неавторизован.",
#             "content": {
#                 "application/json": {
#                     "example": {"detail": "Некорректные учетные данные"}
#                 }
#             },
#         },
#     },
# )
# async def custom_login(form_data: OAuth2PasswordRequestForm = Depends()):
#     try:
#         # Используем backend для аутентификации
#         user = await authentication_backend.authenticate(credentials=form_data)
#         if not user:
#             raise HTTPException(status_code=401, detail="Некорректные учетные данные")
#
#         # Генерация токена
#         token = await fastapi_users.authenticator.backend.login(user)
#         return JSONResponse(
#             {"access_token": token["access_token"], "token_type": "bearer"}
#         )
#     except (UserNotExists, InvalidPasswordException):
#         raise HTTPException(status_code=400, detail="Некорректные учетные данные")


# /register
router.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)


# /request-verify-token
# /verify
router.include_router(
    fastapi_users.get_verify_router(
        UserRead,
    ),
)

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
