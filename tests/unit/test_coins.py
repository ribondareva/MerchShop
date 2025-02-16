import pytest
import pytest_asyncio
from httpx import AsyncClient


# Инициализация асинхронного клиента FastAPI
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://localhost:8080") as client:
        yield client


# Функция для создания пользователя и получения токена
async def create_user_and_get_token(client, username, password):
    response = await client.post(
        "/api/auth/",  # Путь для авторизации
        params={  # Параметры передаются через query-строку
            "username": username,
            "password": password,
            "email": "user@user.com",
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
        },
    )
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token
    return token


# Фикстура для токена отправителя
@pytest_asyncio.fixture
async def sender_token(client):
    return await create_user_and_get_token(client, "sender_user3", "password3")


# Тест успешного перевода монеток
@pytest.mark.asyncio
async def test_transfer_coins(client, sender_token):
    receiver_id = "849665ad-2802-41c0-bf10-11bd7c2d7f2b"
    response = await client.post(
        "/api/sendCoin/",
        json={"to_user_id": receiver_id, "amount": 5},
        headers={"Authorization": f"Bearer {sender_token}"},
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 5


# Тест на недостаточный баланс
@pytest.mark.asyncio
async def test_transfer_insufficient_balance(client, sender_token):
    receiver_id = "849665ad-2802-41c0-bf10-11bd7c2d7f2b"
    response = await client.post(
        "/api/sendCoin/",
        json={"to_user_id": receiver_id, "amount": 10000},
        headers={"Authorization": f"Bearer {sender_token}"},
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Неверный запрос"
