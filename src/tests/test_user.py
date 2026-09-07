import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    response = await client.post("/users", json={"email": "testuser@example.com", "password": "testpass"})
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@example.com"

@pytest.mark.asyncio
async def test_create_user_invalid_email(client: AsyncClient) -> None:
    response = await client.post("/users", json={"email": "invalidemail", "password": "testpass"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_missing_password(client: AsyncClient) -> None:
    response = await client.post("/users", json={"email": "testuser@example.com"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_missing_email(client: AsyncClient) -> None:
    response = await client.post("/users", json={"password": "testpass"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_user_short_password(client: AsyncClient) -> None:
    response = await client.post("/users", json={"email": "testuser@example.com", "password": "short"})
    assert response.status_code == 422