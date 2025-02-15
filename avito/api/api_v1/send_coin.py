from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.api_v1.fastapi_users_router import fastapi_users
from core.config import settings

from core.models import Transaction
from core.models import db_helper
from core.models import User
from schemas.requests import TransferCoinsRequest
from schemas.transaction import TransactionResponse
from schemas.responses import ErrorResponse

router = APIRouter(
    prefix=settings.api.v1.send_coin,
    tags=["Transactions"],
)


@router.post(
    "/",
    summary="Отправить монеты другому пользователю.",
    response_model=TransactionResponse,
    responses={
        200: {
            "description": "Успешный ответ.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/TransactionResponse"}
                }
            },
        },
        400: {
            "description": "Неверный запрос.",
            "model": ErrorResponse,
        },
        401: {
            "description": "Неавторизован.",
            "model": ErrorResponse,
        },
        404: {
            "description": "Получатель не найден.",
            "model": ErrorResponse,
        },
        500: {
            "description": "Внутренняя ошибка сервера.",
            "model": ErrorResponse,
        },
    },
)
async def send_coin(
    request: TransferCoinsRequest,
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):

    # Проверка существования получателя
    receiver = await session.scalar(select(User).where(User.id == request.to_user_id))
    if not receiver:
        raise HTTPException(status_code=404, detail="Получатель не найден")

    # Проверка баланса отправителя
    if user.balance < request.amount:
        raise HTTPException(status_code=400, detail="Неверный запрос")

    # Обновляем балансы
    user.balance -= request.amount
    receiver.balance += request.amount

    # Создаем транзакцию
    transaction = Transaction(
        sender_id=user.id, receiver_id=receiver.id, amount=request.amount
    )
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return TransactionResponse.from_orm(transaction)
