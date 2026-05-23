# purpose: Python structured logger with OTel + redaction adapter.
# consumes: see content/02-output-contract.xml inputs for structured-logging-as-code
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-700 tokens when loaded as context
from __future__ import annotations
import json
import logging
import os
import sys
import time
from typing import Any

try:
    from opentelemetry.trace import get_current_span
except Exception:
    def get_current_span():
        return None


REDACT_FIELDS = {"password", "secret", "token", "card_number"}


def _redact(d: Any) -> Any:
    if isinstance(d, dict):
        return {k: ("***" if k in REDACT_FIELDS else _redact(v)) for k, v in d.items()}
    if isinstance(d, list):
        return [_redact(x) for x in d]
    return d


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        span = get_current_span()
        ctx = span.get_span_context() if span else None
        payload = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "msg": record.getMessage(),
            "service": os.environ.get("SERVICE", "unknown"),
            "env": os.environ.get("ENV", "dev"),
            "request_id": getattr(record, "request_id", None),
            "trace_id": f"{ctx.trace_id:032x}" if ctx else None,
            "span_id": f"{ctx.span_id:016x}" if ctx else None,
            "fields": _redact(getattr(record, "fields", {})),
        }
        return json.dumps({k: v for k, v in payload.items() if v is not None})


def build_logger(name: str) -> logging.Logger:
    log = logging.getLogger(name)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(JsonFormatter())
    log.addHandler(h)
    log.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    return log
