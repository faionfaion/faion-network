"""
Minimal fast input moderation: rule-based injection check + OpenAI Moderation API.

Usage:
    is_safe, reasons = moderate_input(user_text)
    if not is_safe:
        return {"error": "Input blocked", "reasons": reasons}
"""
import re
from openai import OpenAI

client = OpenAI()

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "disregard your",
    "you are now",
    "act as",
]


def moderate_input(text: str) -> tuple[bool, list[str]]:
    """Returns (is_safe, reasons). Fast rule-based + OpenAI moderation."""
    issues = []

    # Rule-based injection check (microseconds)
    for pattern in INJECTION_PATTERNS:
        if pattern in text.lower():
            issues.append("prompt_injection_signal")
            break

    # API-based content moderation (~100ms, free)
    result = client.moderations.create(input=text)
    if result.results[0].flagged:
        cats = [k for k, v in result.results[0].categories.model_dump().items() if v]
        issues.append(f"moderation_flagged:{','.join(cats)}")

    return len(issues) == 0, issues
