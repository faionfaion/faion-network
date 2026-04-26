# vui_privacy.py — VUI disclosure emitter and PII redactor
# Input: jurisdiction string -> disclosure text
# Input: transcript text -> redacted text (PII replaced with [type] tokens)
import re

DISCLOSURES = {
    "gdpr": (
        "I'll record this conversation to help you. You can say 'stop recording' anytime, "
        "or ask 'what data do you keep?' I won't use this for ads."
    ),
    "hipaa": (
        "This call may discuss health information. I'll keep it confidential and you can "
        "request deletion at any time."
    ),
    "ccpa": (
        "I may collect voice data to process your request. You have the right to know, "
        "delete, and opt out of sale of personal information."
    ),
}

PII_PATTERNS = {
    "card":  re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "phone": re.compile(r"\b(?:\+?\d[\d \-]{7,}\d)\b"),
    "ssn":   re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "dob":   re.compile(r"\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b"),
}


def disclose(jurisdiction: str) -> str:
    """Return the disclosure string for the given jurisdiction.
    Falls back to GDPR wording when jurisdiction is unknown.
    """
    return DISCLOSURES.get(jurisdiction.lower(), DISCLOSURES["gdpr"])


def redact(text: str) -> str:
    """Replace detected PII patterns with [TYPE] tokens.
    Apply before any logging or persistence call.
    """
    for label, pattern in PII_PATTERNS.items():
        text = pattern.sub(f"[{label}]", text)
    return text


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3 and sys.argv[1] == "disclose":
        print(disclose(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == "redact":
        print(redact(sys.argv[2]))
    else:
        print("Usage: python vui_privacy.py disclose <jurisdiction>")
        print("       python vui_privacy.py redact '<text>'")
