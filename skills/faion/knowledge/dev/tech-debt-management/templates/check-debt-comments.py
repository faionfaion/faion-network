#!/usr/bin/env python3
"""check-debt-comments.py — pre-commit hook.
Rejects commits with unlinked TODO/FIXME/HACK/XXX/TECH_DEBT markers.
Required format: TODO(PROJ-123): description
Usage: add to .pre-commit-config.yaml, entry: python scripts/check-debt-comments.py
"""
import re
import sys

DEBT_PATTERN = re.compile(r'\b(TODO|FIXME|HACK|XXX|TECH_DEBT)\b')
TICKET_PATTERN = re.compile(r'\b(TODO|FIXME|HACK|XXX|TECH_DEBT)\s*\([A-Z]+-\d+\)')


def check_file(filepath: str) -> bool:
    try:
        content = open(filepath).read()
    except (OSError, UnicodeDecodeError):
        return True  # skip binary or unreadable

    debt_markers = DEBT_PATTERN.findall(content)
    ticketed_markers = TICKET_PATTERN.findall(content)

    if len(debt_markers) > len(ticketed_markers):
        print(f"{filepath}: debt marker without ticket reference")
        print("  Required format: TODO(PROJ-123): description")
        return False
    return True


if __name__ == "__main__":
    all_good = all(check_file(f) for f in sys.argv[1:])
    sys.exit(0 if all_good else 1)
