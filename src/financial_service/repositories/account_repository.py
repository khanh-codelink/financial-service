from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from financial_service.models.account_model import AccountModel

# Correct use for database operations in the repository class for better separation of concerns and maintainability.
# Add logging for better debugging and monitoring of database operations.
class AccountRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_account_by_id(self, account_id: int) -> AccountModel | None:
        stmt = select(AccountModel).where(AccountModel.id == account_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_account(self, account: AccountModel) -> AccountModel:
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account

    async def update_account(self, account: AccountModel) -> AccountModel:
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account

    async def get_accounts_by_user_id(self, user_id: int) -> list[AccountModel]:
        stmt = select(AccountModel).where(AccountModel.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()