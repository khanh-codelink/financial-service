from financial_service.repositories.user_repository import UserRepository
from financial_service.schemas import UserSummaryResponse

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.userRepository = user_repository

    async def get_user(self, user_id):
        return await self.userRepository.get_user(user_id)

    async def get_user_summary(self, user_id) -> UserSummaryResponse:
        user = await self.userRepository.get_user(user_id)
        if not user:
            return None

        if not user.accounts:
            return UserSummaryResponse(
                id=user.id,
                email=user.email,
                accountNumber=0,
                totalBalance=0,
                totalTransactions=0
            )

        return UserSummaryResponse(
            id=user.id,
            email=user.email,
            accountNumber=len(user.accounts),
            totalBalance=sum(account.balance for account in user.accounts),
            totalTransactions=sum(len(account.transactions) for account in user.accounts)
        )