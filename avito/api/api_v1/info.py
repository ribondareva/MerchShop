from fastapi import APIRouter, Depends

from api.api_v1.fastapi_users_router import fastapi_users
from core.config import settings
from core.models import User, Purchase, Transaction, db_helper

from schemas.responses import InfoResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


router = APIRouter(
    prefix=settings.api.v1.info,
    tags=["Info"],
)


@router.get(
    "/",
    responses={
        200: {
            "description": "Успешный ответ.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/InfoResponse"}
                }
            },
        },
        400: {
            "description": "Неверный запрос.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                    "example": {"errors": "Неверный запрос."},
                }
            },
        },
        401: {
            "description": "Неавторизован.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                    "example": {"errors": "Требуется авторизация."},
                }
            },
        },
        500: {
            "description": "Внутренняя ошибка сервера.",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                    "example": {"errors": "Произошла ошибка на сервере."},
                }
            },
        },
    },
    response_model=InfoResponse,
    summary="Получить информацию о монетах, инвентаре и истории транзакций.",
)
async def get_user_info(
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    # Получаем баланс
    balance = user.balance

    # Получаем инвентарь
    purchases_query = await session.execute(
        select(Purchase).filter(Purchase.user_id == user.id)
    )
    purchases = purchases_query.scalars().all()
    inventory = [{"item": p.merch_item.name} for p in purchases]

    # Получаем историю транзакций
    received_query = await session.execute(
        select(Transaction).filter(Transaction.receiver_id == user.id)
    )
    sent_query = await session.execute(
        select(Transaction).filter(Transaction.sender_id == user.id)
    )

    coin_history = {
        "received": [
            {"from_user": t.sender.username, "amount": t.amount}
            for t in received_query.scalars().all()
        ],
        "sent": [
            {"to_user": t.receiver.username, "amount": t.amount}
            for t in sent_query.scalars().all()
        ],
    }

    return InfoResponse(coins=balance, inventory=inventory, coinHistory=coin_history)
