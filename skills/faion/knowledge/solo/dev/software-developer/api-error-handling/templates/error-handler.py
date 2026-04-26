"""Global exception handlers for FastAPI — RFC 7807 Problem Detail responses."""
import uuid
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    trace_id: str | None = None
    errors: list[dict] | None = None


app = FastAPI()


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content=ProblemDetail(
            type="https://api.example.com/errors/validation-error",
            title="Validation Error",
            status=400,
            detail="Request validation failed",
            instance=str(request.url.path),
            trace_id=str(uuid.uuid4()),
            errors=[
                {"field": e["loc"][-1], "code": e["type"], "message": e["msg"]}
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
            type="https://api.example.com/errors/internal-error",
            title="Internal Server Error",
            status=500,
            detail="An unexpected error occurred",
            instance=str(request.url.path),
            trace_id=str(uuid.uuid4()),
        ).model_dump(),
    )
