from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from financial_service.database.database import get_db
from financial_service.schemas import UserCreate, UserResponse
from financial_service.models.user_model import UserModel
from financial_service.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])
default_db: AsyncSession = Depends(get_db)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = default_db) -> UserModel:
    
    user = UserModel(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = default_db) -> UserModel:
    # user = await db.get(UserModel, user_id)

    stmt = await db.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    user = stmt.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user