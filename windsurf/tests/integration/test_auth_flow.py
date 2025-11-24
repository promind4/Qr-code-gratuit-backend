import pytest
from httpx import AsyncClient

from src.core.security import hash_password
from src.core.security import fake_users_db


@pytest.mark.asyncio
async def test_token_endpoint_returns_jwt(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/token",
        json={"username": "developer", "password": "devpass123"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert "access_token" in payload
    assert payload["token_type"] == "bearer"
    assert payload["expires_in"] == 1440 * 60


@pytest.mark.asyncio
async def test_token_endpoint_rejects_invalid_credentials(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/token",
        json={"username": "developer", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides"
