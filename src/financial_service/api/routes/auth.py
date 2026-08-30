from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from financial_service.database.database import get_db
from financial_service.models.user_model import UserModel
from financial_service.utils.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)
              ) -> dict[str, str]:
    """Endpoint to authenticate a user and provide an access token."""
    stmt = select(UserModel).where(UserModel.email == form_data.username)
    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}