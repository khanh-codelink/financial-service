from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from financial_service.models.account_model import AccountModel

from financial_service.models.base_model import Base

class TransactionType(StrEnum):
    CREDIT = "credit"
    DEBIT = "debit"

class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

class TransactionModel(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType), nullable=False)    
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 nullable=False)

    account: Mapped["AccountModel"] = relationship(back_populates="transactions")