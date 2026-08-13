# Structured Logging Patterns

## Summary

**One-sentence:** Emit structured JSON logs with correlation IDs, level discipline, masked sensitive fields, and middleware-attached context for every request.

**One-paragraph:** Logs are JSON objects, never plain text. Every request carries a correlation_id propagated via middleware; every log line includes it. Levels follow a contract (ERROR for actionable, WARN for degraded, INFO for state changes, DEBUG for verbose). Sensitive fields (PII, secrets, tokens) are masked in a single pipeline stage. Logs ship to an aggregator (Loki, ELK, Datadog). Output is the logging module + middleware + redaction rules.

**Ефективно для:**

- Backend services where log volume + searchability matter.
- Multi-service architectures needing request tracing.
- Compliance contexts requiring PII redaction.
- Replacing print/log.info('...') with reviewable structured calls.

## Applies If (ALL must hold)

- Service emits logs as part of its operational story.
- Log aggregator exists (Loki, ELK, Datadog, Cloud Logging).
- Requests have an identifiable boundary (HTTP request, message consumption, worker job).
- PII or secrets may appear in logged payloads.

## Skip If (ANY kills it)

- Single-binary CLI where stderr is the only output channel.
- Embedded systems with no aggregator and constrained memory.
- Services that emit only metrics + traces, no logs by design.
- Logs go to a managed service that owns redaction + structure entirely.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Logging library chosen per language (structlog, zap, slog, winston) | config | platform |
| Log aggregator endpoint + index schema | config | platform |
| PII field list to redact (emails, phones, tokens) | policy | security |
| Correlation-ID source: request header, generated UUID, parent context | ADR | tech-lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-error-handling]] | Error logs carry structured fields matching error chain. |
| [[go-error-handling-patterns]] | Error wrapping preserves fields the logger surfaces. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (JSON output, correlation_id everywhere, level discipline, no PII in logs, single redaction pipeline, no print statements) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for logging module spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: pick library → middleware → redaction → level audit → aggregator | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `middleware_wiring` | sonnet | Plug correlation_id into request context. |
| `redaction_rules` | sonnet | Field-list-driven redaction pipeline. |
| `level_audit` | sonnet | Walk existing log calls; reclassify by contract. |

## Templates

| File | Purpose |
|------|---------|
| `templates/structlog-config.py` | structlog (Python) config with JSON renderer + processors |
| `templates/request-middleware.py` | Middleware: bind correlation_id + request context |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-logging-patterns.py` | Validate logging module spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[api-error-handling]]
- [[go-error-handling-patterns]]
- [[django-celery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps service architecture, log destination, and PII exposure to a rule from `01-core-rules.xml`, telling the agent whether to apply the conventions or skip for managed/CLI cases. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/structlog-config.py`

```python
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
```

### `templates/request-middleware.py`

```python
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
```
