import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from financial_service.database.database import init_db
from financial_service.api.router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    yield

app = FastAPI(title="Financial Service API", version="1.0.0", lifespan=lifespan)
app.include_router(api_router)


# For testing the API connectivity
@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}

@app.get("/delayed_ping")
async def delayed_ping() -> dict[str, str]:
    delay = 2
    await asyncio.sleep(delay)
    return {"message": f"pong after delay {delay}s"}
