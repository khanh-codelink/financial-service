from fastapi import HTTPException
from financial_service.repositories.account_repository import AccountRepository
from financial_service.models.user_model import UserModel
from financial_service.models.transaction_model import TransactionModel
from financial_service.repositories.account_repository import AccountRepository
from financial_service.repositories.transaction_repository import TransactionRepository
from financial_service.schemas import TransactionCreate


class TransactionService:
    def __init__(self, repository: TransactionRepository, accountRepository: AccountRepository):
        self.repository = repository
        self.accountRepository = accountRepository

    async def create_transaction(self, payload: TransactionCreate, current_user: UserModel) -> TransactionModel:
        account = await self.accountRepository.get_account_by_id(payload.account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found or does not belong to the current user")

        if payload.type == "DEBIT" and account.balance < payload.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        payload.account_id = account.id
        
        return await self.repository.create_transaction(payload, account)