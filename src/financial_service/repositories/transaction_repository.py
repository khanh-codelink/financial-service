from sqlalchemy.ext.asyncio import AsyncSession

from financial_service.api.routes import transaction
from financial_service.models.account_model import AccountModel
from financial_service.models.transaction_model import TransactionModel, TransactionType
from financial_service.schemas import TransactionCreate


class TransactionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_transaction(self, 
                                 payload: TransactionCreate,
                                 account: AccountModel
                                 ) -> TransactionModel:

        if payload.type == TransactionType.DEBIT:
            account.balance -= payload.amount
        else:
            account.balance += payload.amount

        transaction = TransactionModel(**payload.model_dump())

        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction