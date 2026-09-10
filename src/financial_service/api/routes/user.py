from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from financial_service.database.database import get_db
from financial_service.repositories.user_repository import UserRepository
from financial_service.schemas import UserCreate, UserResponse, UserSummaryResponse
from financial_service.models.user_model import UserModel
from financial_service.services.user_service import UserService
from financial_service.utils.deps import get_current_user
from financial_service.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])
default_db: AsyncSession = Depends(get_db)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = default_db) -> UserModel:
    """Endpoint to create a new user."""
    
    user = UserModel(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get("/summary", response_model=UserSummaryResponse)
async def get_user_summary(current_user: UserModel = Depends(get_current_user), db: AsyncSession = default_db) -> UserSummaryResponse:
    """Endpoint to retrieve a summary of a user by their ID."""

    repository = UserRepository(db)
    service = UserService(repository)

    summary = await service.get_user_summary(current_user.id)
    return summary

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = default_db) -> UserResponse:
    """Endpoint to retrieve a user by their ID."""

    repository = UserRepository(db)
    service = UserService(repository)

    return await service.get_user(user_id)