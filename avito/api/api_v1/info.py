from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import joinedload

from api.api_v1.fastapi_users_router import fastapi_users
from core.config import settings
from core.models import User, Purchase, Transaction, db_helper

from schemas.responses import InfoResponse, ErrorResponse, CoinHistory

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
        select(Purchase)
        .options(joinedload(Purchase.merch_item))  # Загружаем связанные товары
        .filter(Purchase.user_id == user.id)
    )
    purchases = purchases_query.scalars().all()
    inventory = [{"item": p.merch_item.name} for p in purchases]

    # Получаем историю полученных монет
    received_query = await session.execute(
        select(Transaction)
        .options(joinedload(Transaction.sender))  # Загружаем отправителя
        .filter(Transaction.receiver_id == user.id)
    )
    received_transactions = received_query.scalars().all()
    received_history = [
        {"from_user": t.sender.username, "to_user": None, "amount": t.amount}
        for t in received_transactions
    ]

    # Получаем историю отправленных монет
    sent_query = await session.execute(
        select(Transaction)
        .options(joinedload(Transaction.receiver))
        .filter(Transaction.sender_id == user.id)
    )
    sent_transactions = sent_query.scalars().all()
    sent_history = [
        {
            "from_user": user.username,
            "to_user": t.receiver.username,
            "amount": t.amount,
        }
        for t in sent_transactions
    ]

    coin_history = CoinHistory(received=received_history, sent=sent_history)

    return InfoResponse(coins=balance, inventory=inventory, coinHistory=coin_history)
