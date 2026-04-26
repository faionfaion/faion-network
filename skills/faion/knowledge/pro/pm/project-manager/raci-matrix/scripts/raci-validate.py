#!/usr/bin/env python3
"""raci-validate.py — check RACI CSV for rule violations.

CSV format: first column = task name, remaining columns = role names.
Cell values: R, A, C, I, A/R (or combinations separated by /).

Checks:
  - Each task has exactly one A
  - Each task has at least one R
  - No task has more than 4 C (bottleneck signal)
  - No row is entirely empty

Usage: python raci-validate.py matrix.csv
Exit 1 if violations found, 0 if clean.
"""
import csv
import sys
from collections import Counter


def parse_cell(c: str) -> set[str]:
    return {x.strip().upper() for x in c.replace("/", ",").split(",") if x.strip()}


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: raci-validate.py <matrix.csv>")

    rows = list(csv.reader(open(sys.argv[1])))
    if not rows:
        sys.exit("Empty CSV")

    header, body = rows[0], rows[1:]
    errors = []

    for row in body:
        if not row:
            continue
        task = row[0]
        cells = [parse_cell(c) for c in row[1:]]
        flat = Counter()
        for s in cells:
            for ch in s:
                flat[ch] += 1

        if flat["A"] == 0:
            errors.append((task, "no Accountable — assign one"))
        if flat["A"] > 1:
            errors.append((task, f"{flat['A']} Accountables — pick exactly one"))
        if flat["R"] == 0:
            errors.append((task, "no Responsible — work will not get done"))
        if flat["C"] > 4:
            errors.append((task, f"{flat['C']} Consulted (> 4 = bottleneck) — reduce"))
        if not any(s for s in cells):
            errors.append((task, "empty row — remove task or assign roles"))

    if errors:
        print(f"RACI violations ({len(errors)} found):")
        for task, msg in errors:
            print(f"  [FAIL] {task!r}: {msg}")
        sys.exit(1)

    print(f"OK: {len(body)} tasks pass all RACI rules.")


if __name__ == "__main__":
    main()
