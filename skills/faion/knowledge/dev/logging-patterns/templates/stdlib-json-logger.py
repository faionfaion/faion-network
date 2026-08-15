# purpose: stdlib-only JSON logger with request_id ContextVar, for projects that cannot add structlog
# consumes: standard library logging records
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml#r1-json-output
# token-budget-impact: ~370 tokens when loaded as context
"""The no-dependency alternative to `structlog-config.py`.

Same contract — JSON out, `request_id` on every line, one formatter — with no
third-party package. Use it when the service cannot take a new dependency;
otherwise prefer the structlog config, whose processor chain is where the
redaction pipeline belongs.
"""
import json
import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any

REQUEST_ID: ContextVar[str] = ContextVar("request_id", default="-")

_RESERVED = {"args", "msg", "levelname", "name", "exc_info", "exc_text", "stack_info"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": self.formatTime(record),
            "level": record.levelname.lower(),
            "event": record.getMessage(),
            "request_id": REQUEST_ID.get(),
            "logger": record.name,
        }
        for key, value in record.__dict__.items():
            if key.startswith("_") or key in payload or key in _RESERVED:
                continue
            payload[key] = value
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def new_request_id() -> str:
    rid = str(uuid.uuid4())
    REQUEST_ID.set(rid)
    return rid


def configure(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
