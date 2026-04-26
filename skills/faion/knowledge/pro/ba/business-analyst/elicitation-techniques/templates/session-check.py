#!/usr/bin/env python3
"""session-check.py — validate elicitation session artifact before commit.

Checks: YAML frontmatter completeness, consent flag, pii_redacted flag,
and common PII patterns in the body. Wire into pre-commit so unredacted
transcripts cannot land.

Usage: python session-check.py path/to/session.md
Exit 0: valid. Exit 1: errors found.
"""
from __future__ import annotations
import sys, json, re, pathlib, yaml

REQUIRED = {"session_id", "technique", "stakeholders", "date",
            "consent", "pii_redacted"}
TECHNIQUES = {"interview", "workshop", "focus_group", "observation",
              "survey", "document_analysis", "prototyping", "brainstorming"}
PII_PATTERNS = [
    re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),    # email
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),            # US SSN
    re.compile(r"\b(?:\d[ -]*?){13,19}\b"),           # card-ish number
]

def load(path: pathlib.Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing YAML frontmatter (must start with ---)")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{path}: malformed frontmatter")
    return yaml.safe_load(parts[1]) or {}, parts[2]

def main(p: str) -> int:
    path = pathlib.Path(p)
    fm, body = load(path)
    errors: list[str] = []
    missing = REQUIRED - set(fm)
    if missing:
        errors.append(f"missing frontmatter fields: {sorted(missing)}")
    if fm.get("technique") not in TECHNIQUES:
        errors.append(f"technique must be one of: {sorted(TECHNIQUES)}")
    if fm.get("consent") is not True:
        errors.append("consent must be true (boolean, not string)")
    if fm.get("pii_redacted") is not True:
        errors.append("pii_redacted must be true — run Presidio pass first")
    leaks = [pat.pattern for pat in PII_PATTERNS if pat.search(body)]
    if leaks:
        errors.append(f"possible PII still present matching: {leaks}")
    result = {"file": str(path), "ok": not errors, "errors": errors}
    print(json.dumps(result, indent=2, default=str))
    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "session.md"))
