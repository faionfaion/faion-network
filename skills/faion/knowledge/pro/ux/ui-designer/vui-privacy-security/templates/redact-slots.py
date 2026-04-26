#!/usr/bin/env python3
# redact-slots.py — strip sensitive slots and PII patterns from ASR transcripts
# Usage: import and call redact(text, slots) before any LLM call or log write
# Returns: (redacted_text, list_of_redacted_field_names)
import re

SENSITIVE_SLOTS = {"ssn", "card_number", "cvv", "dob", "mrn", "pin", "password", "account_number"}

PATTERNS: dict[str, re.Pattern] = {
    "card_number": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "ssn":         re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone":       re.compile(r"\+?\d[\d \-]{8,14}\d"),
    "email":       re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Z|a-z]{2,}\b"),
}


def redact(text: str, slots: dict) -> tuple[str, list[str]]:
    """
    Args:
        text: raw ASR transcript string
        slots: dict of slot_name -> slot_value from the dialog manager

    Returns:
        (redacted_text, list of field names that were redacted)
    """
    redacted_fields: list[str] = []

    # Redact known sensitive slot values first (exact match)
    for slot, val in list(slots.items()):
        if slot in SENSITIVE_SLOTS and val:
            text = text.replace(str(val), f"<{slot.upper()}>")
            redacted_fields.append(slot)

    # Redact patterns (partial numbers, emails, phones)
    for label, pat in PATTERNS.items():
        if pat.search(text):
            text = pat.sub(f"<{label.upper()}>", text)
            redacted_fields.append(label)

    return text, redacted_fields
