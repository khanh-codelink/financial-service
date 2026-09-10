from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from financial_service.models.account_model import AccountModel
from financial_service.models.user_model import UserModel


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_user(self, user_id):
        stmt = (select(UserModel)
                .options(selectinload(UserModel.accounts)
                  .selectinload(AccountModel.transactions))
                .where(UserModel.id == user_id))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()