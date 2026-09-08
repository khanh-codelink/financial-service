import pytest
from httpx import AsyncClient
from financial_service.models.user_model import UserModel
from tests.conftest import create_account
pytestmark = pytest.mark.integration
@pytest.mark.asyncio
async def test_unauthenticated_transaction_fail(client: AsyncClient) -> None:
    response = await client.post("/transactions", json={
        "account_id": 2,
        "amount": 100, 
        "type": "credit"
        })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_authenticated_transaction_credit_success(client: AsyncClient, user_a: UserModel, auth_header_a: dict[str, str], create_account) -> None:
    account = await create_account(user_id=user_a.id, initial_balance=100.0)
    response = await client.post("/transactions", json={
        "account_id": account.id,
        "amount": 100, 
        "type": "credit"
        }, headers=auth_header_a)
    assert response.status_code == 200
    accountAfter = await client.get(f"/accounts/{account.id}", headers=auth_header_a)
    assert accountAfter.status_code == 200
    data = accountAfter.json()
    assert data["balance"] == "200.00"

@pytest.mark.asyncio
async def test_authenticated_transaction_debit_success(client: AsyncClient, user_a: UserModel, auth_header_a: dict[str, str], create_account) -> None:
    account = await create_account(user_id=user_a.id, initial_balance=200.0)
    response = await client.post("/transactions", json={
        "account_id": account.id,
        "amount": 100, 
        "type": "debit"
        }, headers=auth_header_a)
    assert response.status_code == 200
    accountAfter = await client.get(f"/accounts/{account.id}", headers=auth_header_a)
    assert accountAfter.status_code == 200
    data = accountAfter.json()
    assert data["balance"] == "100.00"

@pytest.mark.asyncio
async def test_authenticated_transaction_debit_fail_insufficient_balance(client: AsyncClient, user_a: UserModel, auth_header_a: dict[str, str], create_account) -> None:
    account = await create_account(user_id=user_a.id, initial_balance=50.0)
    response = await client.post("/transactions", json={
        "account_id": account.id,
        "amount": 100, 
        "type": "debit"
        }, headers=auth_header_a)
    assert response.status_code == 400
    accountAfter = await client.get(f"/accounts/{account.id}", headers=auth_header_a)
    assert accountAfter.status_code == 200
    data = accountAfter.json()
    assert data["balance"] == "50.00"