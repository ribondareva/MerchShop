from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import MerchItem

INITIAL_MERCH = [
    {"name": "t-shirt", "price": 80},
    {"name": "cup", "price": 20},
    {"name": "book", "price": 50},
    {"name": "pen", "price": 10},
    {"name": "powerbank", "price": 200},
    {"name": "hoody", "price": 300},
    {"name": "umbrella", "price": 200},
    {"name": "socks", "price": 10},
    {"name": "wallet", "price": 50},
    {"name": "pink-hoody", "price": 500},
]


async def init_merch_items(session: AsyncSession):
    for item in INITIAL_MERCH:
        exists = await session.execute(
            select(MerchItem).where(MerchItem.name == item["name"])
        )
        if not exists.scalars().first():
            session.add(MerchItem(name=item["name"], price=item["price"]))
    await session.commit()
