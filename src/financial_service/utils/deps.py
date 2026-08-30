import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from financial_service.database.database import get_db
from financial_service.models.user_model import UserModel
from financial_service.utils.security import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), 
                           db: AsyncSession = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=401,
        detail="User not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            print("User ID not found in token payload")
            raise credentials_exception
    except jwt.PyJWTError:
        print("Failed to decode JWT token")
        raise credentials_exception

    print("Decoded user ID from token:", user_id)
    user = await db.get(UserModel, user_id)
    if user is None:
        raise credentials_exception
    return user