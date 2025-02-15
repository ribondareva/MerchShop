from api.dependencies.authentification.strategy import get_jwt_strategy
from core.authentication.user_manager import UserManager
from core.config import settings
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from api.dependencies.authentification.user_manager import get_user_manager
from schemas.responses import ErrorResponse, AuthResponse
from schemas.user import UserCreate

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)


@router.post(
    "/login",
    summary="Аутентификация и получение JWT токена.",
    responses={
        200: {
            "description": "Успешная аутентификация.",
            "model": AuthResponse,
        },
        400: {
            "description": "Неверный запрос.",
            "model": ErrorResponse,
        },
        401: {
            "description": "Неавторизован.",
            "model": ErrorResponse,
        },
        500: {
            "description": "Внутренняя ошибка сервера.",
            "model": ErrorResponse,
        },
    },
)
async def auth_login(
    user_create: UserCreate = Depends(),
    user_manager: UserManager = Depends(get_user_manager),
):
    user = await user_manager.get_by_username(user_create.username)

    if not user:
        # Если пользователя нет, создаем нового
        user = await user_manager.create(user_create)
        # Генерация JWT токена для нового пользователя
        jwt_strategy = get_jwt_strategy()
        token = await jwt_strategy.write_token(user)
        return JSONResponse(
            status_code=200, content={"access_token": token, "token_type": "bearer"}
        )

    # Если пользователь существует, проверяем пароль
    valid_password = await user_manager.verify_password(
        user_create.password, user.hashed_password
    )
    if not valid_password:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # Генерация JWT токена для существующего пользователя
    jwt_strategy = get_jwt_strategy()
    token = await jwt_strategy.write_token(user)

    return JSONResponse(
        status_code=200, content={"access_token": token, "token_type": "bearer"}
    )
