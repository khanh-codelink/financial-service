from fastapi import APIRouter

from .routes import account, auth, transaction, user, health

router = APIRouter()
router.include_router(auth.router)
router.include_router(account.router)
router.include_router(transaction.router)
router.include_router(user.router)
router.include_router(health.health_router)