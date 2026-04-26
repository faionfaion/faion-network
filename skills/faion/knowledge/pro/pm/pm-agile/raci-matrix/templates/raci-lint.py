#!/usr/bin/env python3
"""raci-lint.py — validate a Markdown RACI table from stdin.

Rules enforced:
  - Exactly one A per task row
  - At least one R per task row
  - Maximum 3 C per task row

Exit 0 if valid, exit 1 if violations found.

Usage:
    python3 raci-lint.py < RACI.md
    cat RACI.md | python3 raci-lint.py
"""
from __future__ import annotations

import sys


def main() -> int:
    text = sys.stdin.read()
    rows = [
        line
        for line in text.splitlines()
        if line.startswith("|") and "---" not in line
    ]
    if len(rows) < 2:
        print("No RACI table found in input.", file=sys.stderr)
        return 2

    # Skip header row
    violations: list[str] = []
    for row in rows[1:]:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < 2:
            continue
        task = cells[0]
        vals = cells[1:]

        a_count = sum(1 for v in vals if "A" in v)
        r_count = sum(1 for v in vals if "R" in v)
        c_count = sum(1 for v in vals if v.strip() == "C")

        if a_count != 1:
            violations.append(f"Row '{task}': A_count={a_count} (must be exactly 1)")
        if r_count < 1:
            violations.append(f"Row '{task}': no R assigned")
        if c_count > 3:
            violations.append(f"Row '{task}': too many C ({c_count}, max 3)")

    if violations:
        for v in violations:
            print(v)
        return 1

    print("RACI table is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
