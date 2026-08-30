from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from financial_service.models.base_model import Base
from sqlalchemy import ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from financial_service.models.transaction_model import TransactionModel

from financial_service.models.user_model import UserModel

class AccountModel(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    owner: Mapped["UserModel"] = relationship(back_populates="accounts")
    transactions: Mapped[list["TransactionModel"]] = relationship(back_populates="account")