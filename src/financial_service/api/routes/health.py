from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from financial_service.database.database import get_db

health_router = APIRouter(prefix="/health", tags=["Operations"])

@health_router.get("/live", status_code=status.HTTP_200_OK)
async def liveness() -> dict[str, str]:
    """Liveness probe: verifies the process is running."""
    return {"status": "alive"}

@health_router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Readiness probe: verifies downstream database connectivity."""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connectivity check failed"
        )