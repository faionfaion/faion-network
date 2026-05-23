#!/usr/bin/env python3
"""Update confidence score for a pattern in patterns.md after task outcome.

Usage: python update-confidence.py .aidocs/memory/patterns.md PAT-001 success
Outcomes: success | partial | failure
"""
import re
import sys


def update_confidence(path: str, pat_id: str, outcome: str) -> None:
    text = open(path).read()
    pattern = rf"(## {re.escape(pat_id)}.*?)(Confidence \| )(\d+\.\d+)"
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        print(f"Pattern {pat_id} not found in {path}")
        return

    old = float(m.group(3))
    if outcome == "success":
        new = min(0.95, old + 0.05)
    elif outcome == "partial":
        new = old * 0.95
    else:
        new = max(0.30, old - 0.15)

    updated = text.replace(
        f"Confidence | {old}",
        f"Confidence | {round(new, 2)}",
        1,
    )
    open(path, "w").write(updated)
    print(f"{pat_id}: {old} -> {round(new, 2)} ({outcome})")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: update-confidence.py <patterns.md> <PAT-NNN> <success|partial|failure>")
        sys.exit(1)
    update_confidence(sys.argv[1], sys.argv[2], sys.argv[3])
