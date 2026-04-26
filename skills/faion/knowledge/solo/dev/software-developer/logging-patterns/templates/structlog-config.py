"""Production structlog configuration with context vars and sensitive data masking."""
import re
from contextvars import ContextVar
from typing import Optional

import structlog

# Context variables — set once per request in middleware
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar("user_id", default=None)

SENSITIVE_FIELDS = {"password", "secret", "token", "api_key", "authorization", "ssn", "credit_card"}
SENSITIVE_PATTERNS = [
    (re.compile(r"\b\d{16}\b"), "****-****-****-****"),
    (re.compile(r"password[\"\\s:=]+[\"']?([^\"'\\s]+)", re.IGNORECASE), "password: [REDACTED]"),
]


def _add_request_context(logger, method_name, event_dict):
    event_dict["request_id"] = request_id_var.get()
    event_dict["user_id"] = user_id_var.get()
    return event_dict


def _mask_sensitive(logger, method_name, event_dict):
    masked = {}
    for key, value in event_dict.items():
        if key.lower() in SENSITIVE_FIELDS:
            masked[key] = "[REDACTED]"
        elif isinstance(value, str):
            for pattern, replacement in SENSITIVE_PATTERNS:
                value = pattern.sub(replacement, value)
            masked[key] = value
        else:
            masked[key] = value
    return masked


structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        _add_request_context,
        _mask_sensitive,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
