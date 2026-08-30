import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_unauthenticated_transaction_fail(client: AsyncClient) -> None:
    response = await client.post("/transactions", json={
        "account_id": 2,
        "amount": 100, 
        "type": "credit"
        })
    assert response.status_code == 401