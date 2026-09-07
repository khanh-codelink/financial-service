import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from financial_service.models.account_model import AccountModel
from financial_service.models.base_model import Base
from financial_service.main import app
from financial_service.database.database import get_db
from financial_service.models.user_model import UserModel
from financial_service.utils.security import hash_password, create_access_token

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def test_db():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session

    await engine.dispose()

@pytest_asyncio.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def user_a(test_db: AsyncSession) -> AsyncGenerator[dict, None]:
    user = UserModel(
        email="user_a@example.com",
        hashed_password=hash_password("passwordForUserA")
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user 

@pytest_asyncio.fixture
async def user_b(test_db: AsyncSession) -> AsyncGenerator[dict, None]:
    user = UserModel(
        email="user_b@example.com",
        hashed_password=hash_password("passwordForUserB")
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user 

@pytest_asyncio.fixture
async def auth_header_a(user_a: UserModel) -> dict[str, str]:
    token = create_access_token({"sub": user_a.email, "user_id": user_a.id})
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def create_account(test_db: AsyncSession):
    async def _factory(user_id: int, initial_balance: float = 0.0):
        account = AccountModel(
            user_id=user_id,
            balance=initial_balance
        )
        test_db.add(account)
        await test_db.commit()
        await test_db.refresh(account)
        return account

    return _factory