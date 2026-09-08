import pytest
from decimal import Decimal
from unittest.mock import AsyncMock

from financial_service.models.account_model import AccountModel
from financial_service.services.transaction_service import TransactionService
from financial_service.schemas import TransactionCreate
from financial_service.models.transaction_model import TransactionType

pytestmark = pytest.mark.unit

@pytest.mark.asyncio
async def test_create_transaction_credit_success() -> None:
    account = type(
        "Account",
        (),
        {"id": 1, "balance": Decimal("100.00")},
    )()
    created_transaction = object()

    account_repository = AsyncMock()
    account_repository.get_account_by_id.return_value = account

    transaction_repository = AsyncMock()
    transaction_repository.create_transaction.return_value = created_transaction

    service = TransactionService(transaction_repository, account_repository)
    payload = TransactionCreate(
        account_id=1,
        amount=Decimal("50.00"),
        type=TransactionType.CREDIT,
    )

    result = await service.create_transaction(payload, current_user=object())

    assert result is created_transaction
    transaction_repository.create_transaction.assert_awaited_once_with(
        payload, account
    )

@pytest.mark.asyncio
async def test_create_transaction_debit_success() -> None:
    account = AccountModel(
        id=1,
        balance=Decimal("100.00")
    )
    account_repo = AsyncMock()
    account_repo.get_account_by_id.return_value = account

    created_transaction = object()
    transaction_repo = AsyncMock()
    transaction_repo.create_transaction.return_value = created_transaction

    service = TransactionService(transaction_repo, account_repo)
    payload = TransactionCreate(
        account_id=1,
        amount=Decimal("50.00"),
        type=TransactionType.DEBIT,
    )

    result = await service.create_transaction(payload, current_user=object())

    assert result is created_transaction
    transaction_repo.create_transaction.assert_awaited_once_with(
        payload, account
    )

@pytest.mark.asyncio
async def test_create_transaction_debit_insufficient_balance() -> None:
    account = AccountModel(
        id=1,
        balance=Decimal("100.00")
    )
    account_repo = AsyncMock()
    account_repo.get_account_by_id.return_value = account

    transaction_repo = AsyncMock()

    service = TransactionService(transaction_repo, account_repo)
    payload = TransactionCreate(
        account_id=1,
        amount=Decimal("150.00"),
        type=TransactionType.DEBIT,
    )

    with pytest.raises(Exception) as e:
        await service.create_transaction(payload, current_user=object())
    assert "Insufficient funds" in str(e.value)

@pytest.mark.asyncio
async def test_create_transaction_account_not_found() -> None:
    account_repo = AsyncMock()
    account_repo.get_account_by_id.return_value = None

    transaction_repo = AsyncMock()

    service = TransactionService(transaction_repo, account_repo)
    payload = TransactionCreate(
        account_id=1,
        amount=Decimal("50.00"),
        type=TransactionType.DEBIT,
    )

    with pytest.raises(Exception) as e:
        await service.create_transaction(payload, current_user=object())
    assert "Account not found" in str(e.value)
