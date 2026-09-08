import pytest
from httpx import AsyncClient
from financial_service.models.user_model import UserModel

pytestmark = pytest.mark.integration

@pytest.mark.asyncio
async def test_login_with_user_a(client: AsyncClient, user_a: UserModel) -> None:
    response = await client.post("/auth/login", data={"username": "user_a@example.com", "password": "passwordForUserA"})
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_failure_with_user_a(client: AsyncClient, user_a: UserModel) -> None:
    response = await client.post("/auth/login", data={"username": "user_a@example.com", "password": "wrongPassword"})
    assert response.status_code == 401
    assert "access_token" not in response.json()

@pytest.mark.asyncio
async def test_login_failure_with_nonexistent_user(client: AsyncClient) -> None:
    response = await client.post("/auth/login", data={"username": "nonexistent@example.com", "password": "somePassword"})
    assert response.status_code == 401
    assert "access_token" not in response.json()