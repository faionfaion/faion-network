# __faion_header_v1__
# purpose: Python structured JSON logger with request_id context
# consumes: see content/02-output-contract.xml
# produces: spec; depends-on: content/01-core-rules.xml#json-structured
# faion_header_json: {"__faion_header__":{"purpose":"Python structured JSON logger with request_id context","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#json-structured","token_budget_impact":"~150 tokens when loaded"}}
import json
import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any

REQUEST_ID: ContextVar[str] = ContextVar("request_id", default="-")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": self.formatTime(record),
            "level": record.levelname.lower(),
            "event": record.getMessage(),
            "request_id": REQUEST_ID.get(),
            "logger": record.name,
        }
        for k, v in getattr(record, "__dict__", {}).items():
            if k.startswith("_") or k in payload or k in {"args", "msg", "levelname", "name"}:
                continue
            payload[k] = v
        return json.dumps(payload, default=str)


def configure() -> None:
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(h)
    root.setLevel(logging.INFO)
