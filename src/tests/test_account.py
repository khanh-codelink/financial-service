import pytest
from httpx import AsyncClient
from financial_service.models.user_model import UserModel
from financial_service.models.account_model import AccountModel

@pytest.mark.asyncio
async def test_create_account_with_user_a(client: AsyncClient, user_a: UserModel, auth_header_a: dict[str, str]) -> None:
    response = await client.post("/accounts", json={"user_id": user_a.id, "balance": 100.0}, headers=auth_header_a)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_a.id
    assert data["balance"] == "100.00"

@pytest.mark.asyncio
async def test_create_account_without_logged_in_user(client: AsyncClient, user_a: UserModel) -> None:
    response = await client.post("/accounts", json={"balance": 200.0})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_account_detail_of_user(client: AsyncClient, user_a: UserModel, auth_header_a: dict[str, str], create_account) -> None:
    account = await create_account(user_id=user_a.id, initial_balance=150.0)
    response = await client.get(f"/accounts/{account.id}", headers=auth_header_a)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_a.id
    assert data["balance"] == "150.00"

@pytest.mark.asyncio
async def test_get_account_detail_of_user_without_logged_in_user(client: AsyncClient, create_account) -> None:
    account = await create_account(user_id=1, initial_balance=150.0)
    response = await client.get(f"/accounts/{account.id}")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_account_detail_of_user_with_invalid_account_id(client: AsyncClient, auth_header_a: dict[str, str]) -> None:
    response = await client.get("/accounts/999999", headers=auth_header_a)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_top_up_account(client: AsyncClient, user_a: UserModel, auth_header_a: dict[str, str], create_account) -> None:
    account = await create_account(user_id=user_a.id, initial_balance=100.0)
    response = await client.put(f"/accounts/{account.id}/top-up", params={"amount": 50.0}, headers=auth_header_a)
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == "150.00"

@pytest.mark.asyncio
async def test_top_up_account_without_logged_in_user(client: AsyncClient, create_account) -> None:
    account = await create_account(user_id=1, initial_balance=100.0)
    response = await client.put(f"/accounts/{account.id}/top-up", params={"amount": 50.0})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_top_up_account_with_invalid_account_id(client: AsyncClient, auth_header_a: dict[str, str]) -> None:
    response = await client.put("/accounts/999999/top-up", params={"amount": 50.0}, headers=auth_header_a)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_edit_account(client: AsyncClient, user_a: UserModel, auth_header_a: dict[str, str], create_account) -> None:
    account = await create_account(user_id=user_a.id, initial_balance=100.0)
    response = await client.put(f"/accounts/{account.id}", json={
        "user_id": user_a.id,
        "balance": 200.0}, headers=auth_header_a)
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == "200.00"

@pytest.mark.asyncio
async def test_edit_account_without_logged_in_user(client: AsyncClient, create_account) -> None:
    account = await create_account(user_id=1, initial_balance=100.0)
    response = await client.put(f"/accounts/{account.id}", json={"balance": 200.0,"user_id": 1})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_edit_account_with_invalid_account_id(client: AsyncClient, auth_header_a: dict[str, str]) -> None:
    response = await client.put("/accounts/999999", json={"balance": 200.0, "user_id": 1}, headers=auth_header_a)
    assert response.status_code == 404