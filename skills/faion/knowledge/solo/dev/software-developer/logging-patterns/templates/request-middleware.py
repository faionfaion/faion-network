"""FastAPI request logging middleware — sets correlation context and logs start/end."""
import time
import uuid

import structlog
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from .structlog_config import request_id_var, user_id_var

logger = structlog.get_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_var.set(request_id)
        user_id_var.set(getattr(request.state, "user_id", None))

        start = time.perf_counter()
        logger.info(
            "request.started",
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None,
        )

        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.info(
                "request.completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
            )
            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as exc:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.error(
                "request.failed",
                method=request.method,
                path=request.url.path,
                duration_ms=duration_ms,
                exc_info=True,
            )
            raise


app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)
