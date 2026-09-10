from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from financial_service.models.transaction_model import TransactionType

class TransactionAccountResponse(BaseModel):
    id: int
    account_id: int
    category_id: int | None = None
    amount: Decimal
    type: TransactionType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AccountCreate(BaseModel):
    user_id: int
    balance: Decimal = Field(default=Decimal("0.00"), ge=0.0)

class AccountResponse(AccountCreate):
    id: int
    created_at: datetime
    transactions: list[TransactionAccountResponse] | None = None

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    accounts: list[AccountResponse] | None = None

    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(BaseModel):
    account_id: int
    category_id: int | None = None
    amount: Decimal = Field(default=Decimal("0.00"), ge=0.0)
    type: TransactionType

class TransactionResponse(TransactionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class TransactionFilterParams(BaseModel):
    account_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    category_id: int | None = None
    min_amount: Decimal | None = Field(None, ge=0)
    max_amount: Decimal | None = Field(None, ge=0)
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    model_config = ConfigDict(from_attributes=True)

class UserSummaryResponse(BaseModel):
    id: int
    email: EmailStr | None = None
    accountNumber: int | None = None
    totalBalance: Decimal | None = None
    totalTransactions: int | None = None

    model_config = ConfigDict(from_attributes=True)