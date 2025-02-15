from api.dependencies.authentification.strategy import get_jwt_strategy
from core.authentication.user_manager import UserManager
from core.config import settings
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from api.dependencies.authentification.user_manager import get_user_manager
from schemas.responses import ErrorResponse, AuthResponse

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
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager),
):
    # Получаем пользователя по имени
    user = await user_manager.get_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # Проверяем пароль
    valid_password = await user_manager.verify_password(
        form_data.password, user.hashed_password
    )
    if not valid_password:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # Получаем JWT стратегию и генерируем токен
    jwt_strategy = get_jwt_strategy()
    token = await jwt_strategy.write_token(user)

    # Возвращаем успешный ответ с токеном
    return JSONResponse(
        status_code=200, content={"access_token": token, "token_type": "bearer"}
    )
