from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from financial_service.models.transaction_model import TransactionType


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AccountCreate(BaseModel):
    user_id: int
    balance: Decimal = Field(default=Decimal("0.00"), ge=0.0)

class AccountResponse(AccountCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(BaseModel):
    account_id: int
    category_id: int | None = None
    amount: Decimal = Field(default=Decimal("0.00"), ge=0.0)
    type: TransactionType

class TransactionResponse(TransactionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)