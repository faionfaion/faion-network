# purpose: Lint questions for leading/double-barreled/loaded patterns
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
#!/usr/bin/env python3
"""
bias_linter.py — deterministic pre-filter for survey question drafts.
Run before LLM bias-review pass to catch patterns the LLM rationalizes away.

Usage:
    cat questions.json | python bias_linter.py
    python bias_linter.py < questions.json

Input (stdin): JSON array of {"text": "question string"} objects.
Output (stdout): JSON array of flagged items with {q, text, flags}.
Exit code: 0 if clean, 1 if any flags found.
"""
import re
import sys
import json

LEADING = re.compile(
    r"\b(don't you (think|agree)|isn't it|wouldn't you say|how amazing|how awful)\b",
    re.IGNORECASE,
)
DOUBLE = re.compile(r"\b(and|or)\b.*\?")  # crude double-barrel heuristic
HYPOTHETICAL = re.compile(
    r"\b(would you|will you|do you plan to|how often will)\b",
    re.IGNORECASE,
)
ABSOLUTIST = re.compile(
    r"\b(always|never|every time|all of the time)\b",
    re.IGNORECASE,
)
MAX_WORDS = 28


def lint(items: list[dict]) -> list[dict]:
    out = []
    for i, q in enumerate(items, 1):
        text = q.get("text", "")
        flags = []
        if LEADING.search(text):
            flags.append("leading")
        if HYPOTHETICAL.search(text):
            flags.append("hypothetical")
        if ABSOLUTIST.search(text):
            flags.append("absolutist-anchor")
        if "?" in text and DOUBLE.search(text) and len(text.split()) > 8:
            # rough check: long question with "and/or" before the "?"
            if "satisf" in text.lower() or "engag" in text.lower():
                flags.append("possible-double-barrel")
        if len(text.split()) > MAX_WORDS:
            flags.append("too-long")
        if flags:
            out.append({"q": i, "text": text, "flags": flags})
    return out


if __name__ == "__main__":
    data = json.load(sys.stdin)  # [{"text": "..."}]
    results = lint(data)
    json.dump(results, sys.stdout, indent=2)
    print()
    if results:
        sys.exit(1)
