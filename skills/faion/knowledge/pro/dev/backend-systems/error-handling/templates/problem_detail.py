# purpose: Legacy template for the error-handling methodology.
# consumes: inputs declared in error-handling/AGENTS.md prerequisites.
# produces: working code/config aligned with content/01-core-rules.xml.
# depends-on: content/02-output-contract.xml schema for output shape.
# token-budget-impact: ~600 tokens when loaded as reference.
# api/errors.py
# RFC 7807 ProblemDetail model + FastAPI exception handlers.
# Replace trace_id placeholder with your actual OTel/Datadog trace context.
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    trace_id: str | None = None
    errors: list[dict] | None = None


def _get_trace_id() -> str:
    """Pull trace ID from OTel context. Replace with your SDK call."""
    try:
        from opentelemetry import trace
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx.is_valid:
            return format(ctx.trace_id, "032x")
    except ImportError:
        pass
    return "unknown"


def _problem(
    request: Request,
    status: int,
    type_slug: str,
    title: str,
    detail: str | None = None,
    errors: list[dict] | None = None,
) -> JSONResponse:
    body = ProblemDetail(
        type=f"https://api.example.com/errors/v1/{type_slug}",
        title=title,
        status=status,
        detail=detail,
        instance=str(request.url.path),
        trace_id=_get_trace_id(),
        errors=errors,
    ).model_dump(exclude_none=True)
    return JSONResponse(
        status_code=status,
        content=body,
        media_type="application/problem+json",
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return _problem(
            request, 422, "validation-error", "Validation Error",
            detail="Request validation failed",
            errors=[
                {"field": e["loc"][-1], "code": e["type"], "message": e["msg"]}
                for e in exc.errors()
            ],
        )

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        # Log full exception server-side; never expose exc to client.
        import logging
        logging.getLogger(__name__).error("Unhandled exception", exc_info=True)
        return _problem(
            request, 500, "internal-error", "Internal Server Error",
            detail="An unexpected error occurred",
        )
