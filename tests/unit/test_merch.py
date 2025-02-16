import pytest
import pytest_asyncio
from httpx import AsyncClient


# Функция для создания пользователя и получения токена
async def create_user_and_get_token(client, username, password):
    response = await client.post(
        "/api/auth/",
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


@pytest_asyncio.fixture
async def sender_token():
    async with AsyncClient(base_url="http://localhost:8080") as client:
        return await create_user_and_get_token(client, "sender_user3", "password3")


@pytest.mark.asyncio
async def test_purchase_merch_success(sender_token):
    # Имитация запроса на покупку
    item_name = "t-shirt"
    async with AsyncClient(base_url="http://localhost:8080") as client:
        response = await client.get(
            f"/api/buy/{item_name}",
            headers={"Authorization": f"Bearer {sender_token}"},
        )

    # Ожидаем успешный ответ
    assert response.status_code == 200
    assert response.json()["detail"] == f"Товар '{item_name}' успешно куплен"


@pytest.mark.asyncio
async def test_purchase_item_not_found(sender_token):
    # Пример запроса на несуществующий товар
    item_name = "NonExistentItem"

    async with AsyncClient(base_url="http://localhost:8080") as client:
        response = await client.get(
            f"/api/buy/{item_name}",
            headers={"Authorization": f"Bearer {sender_token}"},
        )

    assert response.status_code == 404
    assert "Товар не найден." in response.json()["detail"]
