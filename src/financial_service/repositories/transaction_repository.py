from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from financial_service.models.account_model import AccountModel
from financial_service.models.transaction_model import TransactionModel, TransactionType
from financial_service.schemas import TransactionCreate, TransactionFilterParams


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

    async def get_filtered_transactions(
        self,
        params: TransactionFilterParams
    ) -> list[TransactionModel]:
        stmt = (select(TransactionModel)
                .join(AccountModel)
                .where(AccountModel.id == params.account_id))

        # Alternative: use graphqlalchemy to build the query dynamically based on the provided filter parameters.
        conditions = []
        if params.start_date:
            conditions.append(TransactionModel.created_at >= params.start_date)
        if params.end_date:
            conditions.append(TransactionModel.created_at <= params.end_date)
        if params.category_id:
            conditions.append(TransactionModel.category_id == params.category_id)
        if params.min_amount:
            conditions.append(TransactionModel.amount >= params.min_amount)
        if params.max_amount:
            conditions.append(TransactionModel.amount <= params.max_amount)

        # When a graphqlalchemy query is built, it can be executed with the database session to retrieve the filtered transactions.
        if conditions:
            stmt = stmt.where(*conditions)

        offset = (params.page - 1) * params.page_size
        stmt = stmt.offset(offset).limit(params.page_size)

        result = await self.db.execute(stmt)
        return result.scalars().all()