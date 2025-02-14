from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.api_v1.fastapi_users_router import fastapi_users
from core.config import settings
from core.models import User, Purchase, db_helper, MerchItem


router = APIRouter(
    prefix=settings.api.v1.buy,
    tags=["Merch"],
)


@router.get(
    "/{item}",
    summary="Купить предмет за монеты.",
    response_description="Успешный ответ.",
    responses={
        200: {"description": "Успешный ответ."},
        400: {
            "description": "Неверный запрос.",
            "content": {
                "application/json": {"example": {"errors": "Недостаточно монет."}}
            },
        },
        401: {
            "description": "Неавторизован.",
            "content": {
                "application/json": {"example": {"errors": "Требуется авторизация."}}
            },
        },
        404: {
            "description": "Товар не найден.",
            "content": {
                "application/json": {"example": {"errors": "Товар не найден."}}
            },
        },
        500: {
            "description": "Внутренняя ошибка сервера.",
            "content": {
                "application/json": {
                    "example": {"errors": "Произошла ошибка на сервере."}
                }
            },
        },
    },
)
async def buy_item(
    item: str,
    user: User = Depends(fastapi_users.current_user()),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    # Проверяем наличие товара
    item_query = await session.execute(select(MerchItem).filter(MerchItem.name == item))
    merch_item = item_query.scalars().first()

    if not merch_item:
        raise HTTPException(status_code=404, detail="Товар не найден.")

    # Проверяем баланс
    if user.balance < merch_item.price:
        raise HTTPException(status_code=400, detail="Недостаточно монет.")

    # Обновляем баланс и добавляем покупку
    user.balance -= merch_item.price
    purchase = Purchase(user_id=user.id, merch_item_id=merch_item.id)
    session.add(purchase)

    await session.commit()
    return {"detail": f"Товар '{item}' успешно куплен"}
