#!/usr/bin/env python3
"""coverage_gaps.py — list ECO tasks with no methodology coverage.

Reads alignment-matrix.csv with columns:
  domain, task_id, enablers, themes, covered_by, evidence_anchor

Exits non-zero if any gaps found. Wire to weekly CI; failures open an issue
assigned to the PM curriculum owner.
"""
from __future__ import annotations
import csv
import pathlib
import sys


def main(path: str = "alignment-matrix.csv") -> int:
    csv_path = pathlib.Path(path)
    if not csv_path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 1
    rows = list(csv.DictReader(csv_path.open()))
    gaps = [r for r in rows if not r.get("covered_by", "").strip()]
    if not gaps:
        print("All ECO tasks covered.")
        return 0
    by_domain: dict[str, int] = {}
    for r in gaps:
        domain = r.get("domain", "unknown")
        by_domain[domain] = by_domain.get(domain, 0) + 1
        print(
            f"GAP {domain:>22} | {r.get('task_id','?'):<12}"
            f"| themes: {r.get('themes','?')}"
        )
    print()
    for d, n in sorted(by_domain.items()):
        print(f"  {d}: {n} gap(s)")
    return 1


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "alignment-matrix.csv"
    sys.exit(main(path))
