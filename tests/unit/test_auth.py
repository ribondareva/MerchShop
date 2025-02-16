from fastapi.testclient import TestClient
from avito.main import main_app


client = TestClient(main_app)


def test_login_success():
    response = client.post(
        "/api/auth/",
        params={
            "username": "unknown",
            "password": "abc",
            "email": "admin@admin.com",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()  # Проверка, что токен возвращается


def test_login_fail():
    response = client.post(
        "/api/auth/",
        params={
            "username": "unknown",
            "password": "wrong_password",
            "email": "unknown@example.com",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )
    assert response.status_code == 401  # Неверные данные должны возвращать 401
    assert "detail" in response.json()  # Проверка, что есть ошибка
