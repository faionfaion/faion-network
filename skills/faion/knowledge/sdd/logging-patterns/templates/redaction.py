# __faion_header_v1__
# purpose: PII redaction patterns: email, phone, credit-card-like
# consumes: see content/02-output-contract.xml
# produces: spec; depends-on: content/01-core-rules.xml#json-structured
# faion_header_json: {"__faion_header__":{"purpose":"PII redaction patterns: email, phone, credit-card-like","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#json-structured","token_budget_impact":"~150 tokens when loaded"}}
import re

PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "phone": re.compile(r"\+?[0-9][0-9 .-]{8,}\d"),
    "card_like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


def redact(text: str) -> str:
    for name, pat in PATTERNS.items():
        text = pat.sub(f"[REDACTED:{name}]", text)
    return text
