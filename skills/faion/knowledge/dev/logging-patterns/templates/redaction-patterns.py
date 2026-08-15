# purpose: Value-level PII redaction patterns (email, phone, card-like) for the single redaction pipeline
# consumes: log event payload after field-name masking
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml#r5-single-redaction-pipeline
# token-budget-impact: ~200 tokens when loaded as context
"""Field-name masking is not enough: PII arrives inside free-text values too.

`structlog-config.py` masks by key (`password`, `token`). This module is the
value-level half of the same single pipeline — it runs inside that one processor,
never at a call site. Applying it recursively is what closes the nested-payload
gap that `fm-pii-in-error-stacktrace` describes.
"""
import re

PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "phone": re.compile(r"\+?[0-9][0-9 .-]{8,}\d"),
    "card_like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


def redact_text(text: str) -> str:
    for name, pattern in PATTERNS.items():
        text = pattern.sub(f"[REDACTED:{name}]", text)
    return text


def redact(value):
    """Recursive over dicts, lists and strings — nested payloads are the leak path."""
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(redact(v) for v in value)
    if isinstance(value, str):
        return redact_text(value)
    return value
