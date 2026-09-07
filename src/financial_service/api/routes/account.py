from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from financial_service.database.database import get_db
from financial_service.models.account_model import AccountModel
from financial_service.schemas import AccountCreate, AccountResponse
from financial_service.utils.deps import get_current_user

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("", response_model=AccountResponse)
async def create_account(payload: AccountCreate,
                         current_user = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)) -> AccountResponse:
    """
    Endpoint to create a new account.

    The account will be associated with the currently authenticated user.
    """
    account = AccountModel(**payload.model_dump())
    account.user_id = current_user.id
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account

@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(account_id: int, 
                      current_user = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)) -> AccountResponse:
    """
    Endpoint to retrieve an account by its ID.

    The account must belong to the currently authenticated user.
    """
    result = await db.execute(select(AccountModel).where(AccountModel.id == account_id, AccountModel.user_id == current_user.id))
    account = result.scalar_one_or_none()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(account_id: int,
                         payload: AccountCreate,
                         current_user = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)) -> AccountResponse:
    """
    Endpoint to update an existing account.

    The account must belong to the currently authenticated user.
    """
    result = await db.execute(select(AccountModel).where(AccountModel.id == account_id, AccountModel.user_id == current_user.id))
    account = result.scalar_one_or_none()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    for key, value in payload.model_dump().items():
        setattr(account, key, value)
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account

@router.put("/{account_id}/top-up", response_model=AccountResponse)
async def top_up_account(account_id: int,
                         amount: Decimal,
                         current_user = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)) -> AccountResponse:
    """
    Endpoint to top up an existing account.

    The account must belong to the currently authenticated user.
    """
    result = await db.execute(select(AccountModel).where(AccountModel.id == account_id, AccountModel.user_id == current_user.id))
    account = result.scalar_one_or_none()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    account.balance += amount
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account