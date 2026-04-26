#!/usr/bin/env python3
"""scenario-lint.py — fail CI on malformed quality attribute scenarios.

Usage: python scenario-lint.py docs/quality/scenarios.md
Exit 0: all scenarios valid.
Exit 1: one or more scenarios have missing parts, no numeric threshold, or TBD placeholders.
"""
import re
import sys
import pathlib

REQUIRED_PARTS = ["source", "stimulus", "environment", "artifact", "response", "response measure"]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: scenario-lint.py <scenarios-file>")
        return 1

    src = pathlib.Path(sys.argv[1]).read_text().lower()
    # Split on scenario headings
    blocks = re.split(r"^#{2,3}\s+scenario", src, flags=re.M)[1:]

    if not blocks:
        print("No scenarios found (expected ## Scenario or ### Scenario headings)")
        return 1

    errors = []
    for i, block in enumerate(blocks, 1):
        missing = [part for part in REQUIRED_PARTS if part not in block]
        if missing:
            errors.append(f"scenario {i}: missing parts: {missing}")
        if not re.search(r"\d", block):
            errors.append(f"scenario {i}: no numeric threshold — response measure must be quantitative")
        if "tbd" in block or "tba" in block:
            errors.append(f"scenario {i}: contains TBD/TBA placeholder — scenario is incomplete")

    for err in errors:
        print(err)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
