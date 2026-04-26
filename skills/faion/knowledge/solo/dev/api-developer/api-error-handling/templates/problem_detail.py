# ProblemDetail Pydantic model and FastAPI exception handler wiring.
# RFC 7807 Problem Details for HTTP APIs.
import uuid
import logging
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

logger = logging.getLogger(__name__)

API_BASE = "https://api.example.com/errors"


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    trace_id: str | None = None
    errors: list[dict] | None = None


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=400,
            content=ProblemDetail(
                type=f"{API_BASE}/validation-error",
                title="Validation Error",
                status=400,
                detail="Request validation failed",
                instance=str(request.url.path),
                trace_id=str(uuid.uuid4()),
                errors=[
                    {
                        "field": e["loc"][-1] if e["loc"] else "unknown",
                        "code": e["type"],
                        "message": e["msg"],
                    }
                    for e in exc.errors()
                ],
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception: %s", exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content=ProblemDetail(
                type=f"{API_BASE}/internal-error",
                title="Internal Server Error",
                status=500,
                detail="An unexpected error occurred",
                instance=str(request.url.path),
                trace_id=str(uuid.uuid4()),
            ).model_dump(),
        )
