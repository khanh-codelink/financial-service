import time
import uuid
from typing import Callable
from fastapi import Request, Response
import structlog
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
        )

        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        logger.info(
            "http_request_completed",
            status_code=response.status_code,
            duration_ms=round(process_time * 1000, 2),
        )

        response.headers["X-Request-ID"] = request_id
        return response