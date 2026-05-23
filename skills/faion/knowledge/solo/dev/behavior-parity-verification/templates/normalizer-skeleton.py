# purpose: starting-point for the diff normalizer the sampler calls per request.
# consumes: raw observable value from legacy or new path.
# produces: canonical form ready for equality compare.
# depends-on: stdlib only (no external libs in the hot path).
# token-budget-impact: ~250 tokens when loaded as context.

from __future__ import annotations

import hashlib
import re
import uuid
from typing import Any


_UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?$")


def quantize_timestamp(s: str) -> str:
    """Drop sub-second precision so independently-generated times can match."""
    if _TS_RE.match(s):
        return s[:19] + "Z"
    return s


def canonicalize_uuid(s: str) -> str:
    """Normalise UUID casing; non-UUIDs pass through."""
    if _UUID_RE.match(s):
        return str(uuid.UUID(s))
    return s


def redact_pii(value: str) -> str:
    """Hash PII rather than persist plaintext. Email-shaped strings only."""
    if "@" in value and "." in value.split("@")[-1]:
        return "pii:" + hashlib.sha1(value.encode()).hexdigest()[:12]
    return value


def normalize(value: Any) -> Any:
    """Recursive canonicalizer. Same code path for legacy and new outputs."""
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        items = [normalize(v) for v in value]
        # Sort only if items are scalar or shape allows deterministic ordering.
        if all(isinstance(i, (str, int, float, bool)) for i in items):
            items = sorted(items, key=lambda x: (type(x).__name__, str(x)))
        return items
    if isinstance(value, str):
        return redact_pii(canonicalize_uuid(quantize_timestamp(value)))
    return value
