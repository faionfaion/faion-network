# purpose: Python structured logger with OTel + redaction adapter.
# consumes: see content/02-output-contract.xml inputs for structured-logging-as-code
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-700 tokens when loaded as context
"""Structured JSON logger with trace context and PII redaction.

Redaction covers the five PII categories the methodology's own rule names —
email, phone, name, payment token, IP — plus credentials. The first version's
`REDACT_FIELDS = {"password", "secret", "token", "card_number"}` covered none of
the five, matched keys exactly and case-sensitively (so `Authorization`,
`access_token` and `cardNumber` all serialised in the clear), and never looked
at the message body at all. Redaction now happens on KEY (substring,
case-insensitive) and on VALUE (patterns), in both `fields` and `msg`.
"""
from __future__ import annotations

import json
import logging
import os
import re
import sys
import time
from typing import Any

try:
    from opentelemetry.trace import get_current_span
except Exception:  # OTel is optional; the logger must work without it
    def get_current_span():
        return None


# Any key CONTAINING one of these (case-insensitive) is redacted whole.
REDACT_KEY_PARTS = (
    # credentials
    "password", "passwd", "secret", "token", "authorization", "api_key", "apikey",
    "cookie", "session",
    # the five PII categories from 01-core-rules.xml
    "email", "phone", "mobile", "first_name", "last_name", "full_name", "surname",
    "card", "pan", "iban", "cvv", "ip", "remote_addr", "x_forwarded_for",
)

# Values that are PII wherever they appear, including inside free-text messages.
_VALUE_PATTERNS = (
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),          # email
    re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)"),                     # phone
    re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)"),                          # card number
    re.compile(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)"),                       # IPv4
    re.compile(r"\b(?:Bearer|Basic)\s+[A-Za-z0-9._~+/=-]+", re.I),             # auth scheme + token
    re.compile(r"\beyJ[A-Za-z0-9._-]{10,}"),                                   # JWT
)


def _key_is_sensitive(key: str) -> bool:
    k = key.lower()
    return any(part in k for part in REDACT_KEY_PARTS)


def _scrub_text(s: str) -> str:
    for pat in _VALUE_PATTERNS:
        s = pat.sub("***", s)
    return s


def _redact(d: Any) -> Any:
    if isinstance(d, dict):
        return {k: ("***" if _key_is_sensitive(str(k)) else _redact(v)) for k, v in d.items()}
    if isinstance(d, list):
        return [_redact(x) for x in d]
    if isinstance(d, str):
        return _scrub_text(d)
    return d


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        span = get_current_span()
        ctx = span.get_span_context() if span else None
        payload = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "msg": _scrub_text(record.getMessage()),
            "service": os.environ.get("SERVICE", "unknown"),
            "env": os.environ.get("ENV", "dev"),
            "request_id": getattr(record, "request_id", None),
            "trace_id": f"{ctx.trace_id:032x}" if ctx and ctx.trace_id else None,
            "span_id": f"{ctx.span_id:016x}" if ctx and ctx.span_id else None,
            "fields": _redact(getattr(record, "fields", {})),
        }
        return json.dumps({k: v for k, v in payload.items() if v is not None})


def build_logger(name: str) -> logging.Logger:
    log = logging.getLogger(name)
    if not log.handlers:  # idempotent under reload
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(JsonFormatter())
        log.addHandler(h)
    log.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    return log
