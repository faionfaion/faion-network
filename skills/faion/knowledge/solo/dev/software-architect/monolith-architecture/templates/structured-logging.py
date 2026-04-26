"""
Structured logging setup for a Python monolith using structlog.
Outputs JSON in production; human-readable in development.
"""

import logging
import sys
import structlog


def configure_logging(environment: str = "production") -> None:
    """Configure structlog for the application.

    Call once at application startup (manage.py, wsgi.py, asgi.py).
    """
    shared_processors = [
        structlog.contextvars.merge_contextvars,          # request_id, user_id per request
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if environment == "production":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


# -------------------------------------------------------------------
# Request middleware: bind correlation ID per request
# -------------------------------------------------------------------
import uuid
from django.utils.deprecation import MiddlewareMixin


class RequestIdMiddleware(MiddlewareMixin):
    """Bind request_id and user_id to structlog context for every request."""

    def process_request(self, request):
        request_id = request.META.get("HTTP_X_REQUEST_ID") or str(uuid.uuid4())
        request.request_id = request_id
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.path,
            method=request.method,
        )

    def process_response(self, request, response):
        if hasattr(request, "request_id"):
            response["X-Request-ID"] = request.request_id
        return response


# -------------------------------------------------------------------
# Usage in feature code
# -------------------------------------------------------------------
log = structlog.get_logger(__name__)


def create_order(user_id: str, items: list) -> dict:
    log.info("order.create.started", user_id=user_id, item_count=len(items))
    try:
        # ... business logic ...
        order_id = "ord-123"
        log.info("order.create.succeeded", user_id=user_id, order_id=order_id)
        return {"order_id": order_id}
    except Exception as exc:
        log.error("order.create.failed", user_id=user_id, error=str(exc), exc_info=True)
        raise
