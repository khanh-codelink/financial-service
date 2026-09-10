from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from financial_service.database.database import get_db
from financial_service.models.user_model import UserModel
from financial_service.repositories.account_repository import AccountRepository
from financial_service.repositories.transaction_repository import TransactionRepository
from financial_service.schemas import TransactionCreate, TransactionResponse, TransactionFilterParams
from financial_service.services.transaction_service import TransactionService
from financial_service.utils.deps import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("", response_model=TransactionResponse)
async def create_transaction(
  payload: TransactionCreate,
  current_user: UserModel = Depends(get_current_user),
  db: AsyncSession = Depends(get_db)
) -> TransactionResponse:
    """
    Endpoint to create a new financial transaction.

    The transaction will be associated with the currently authenticated user and their account.
    """
    repository = TransactionRepository(db)
    accountRepository = AccountRepository(db)
    service = TransactionService(repository, accountRepository)
    transaction = await service.create_transaction(payload, current_user)
    return transaction

@router.get("", response_model=list[TransactionResponse])
async def list_transactions(
    filter_params: TransactionFilterParams,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> list[TransactionResponse]:
    """
    Endpoint to list all financial transactions for the currently authenticated user.
    """
    repository = TransactionRepository(db)
    accountRepository = AccountRepository(db)
    service = TransactionService(repository, accountRepository)
    transactions = await service.list_transactions(current_user, filter_params)
    return transactions