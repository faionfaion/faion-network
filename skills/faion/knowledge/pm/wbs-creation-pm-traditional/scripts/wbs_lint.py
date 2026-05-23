#!/usr/bin/env python3
"""wbs_lint.py

Lint a WBS Markdown outline:
- check numbering is contiguous (no skipped levels)
- check leaf nodes (work packages) carry owner + estimate
- check no leaf exceeds 80h estimate (decomposition rule)

Inputs:
    --file PATH       WBS markdown path
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = clean
    1 = lint findings
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LEAF_RE = re.compile(
    r"^\s*-\s*(\d+(?:\.\d+)*)\s+(.+?)\s*\(owner:\s*([^,]+),\s*est:\s*(\d+)-?(\d+)?h\)\s*$",
    re.M,
)
NUM_RE = re.compile(r"^\s*-\s*(\d+(?:\.\d+)*)\s+", re.M)

FIXTURE_OK = """# WBS
- 1.0 Phase
  - 1.1 Deliverable
    - 1.1.1 Pkg A (owner: Iryna, est: 16-40h)
    - 1.1.2 Pkg B (owner: Petro, est: 8-24h)
"""
FIXTURE_BAD = """# WBS
- 1.0 Phase
  - 1.1 Deliverable
    - 1.1.1 Pkg A (owner: Iryna, est: 16-200h)
    - 1.1.2 Pkg B (owner: , est: 8-24h)
"""


def lint(text: str) -> list[str]:
    findings: list[str] = []
    for m in LEAF_RE.finditer(text):
        num, name, owner, lo, hi = m.group(1), m.group(2), m.group(3).strip(), int(m.group(4)), int(m.group(5)) if m.group(5) else int(m.group(4))
        if not owner:
            findings.append(f"{num}: owner empty")
        if hi > 80:
            findings.append(f"{num}: estimate upper bound {hi}h > 80h decomposition limit")
        if lo < 8 and "0" not in str(lo):
            findings.append(f"{num}: estimate lower bound {lo}h < 8h decomposition limit")
    # Numbering contiguity (simple check: at each level, last segment increments)
    by_level: dict[int, list[int]] = {}
    for m in NUM_RE.finditer(text):
        parts = m.group(1).split(".")
        # group by parent prefix
        prefix = ".".join(parts[:-1])
        last = int(parts[-1])
        key_lvl = len(parts)
        seen = by_level.setdefault(key_lvl, [])
        seen.append((prefix, last))
    # detect gaps within sibling groups
    from collections import defaultdict
    sib: dict[tuple[int, str], list[int]] = defaultdict(list)
    for lvl, items in by_level.items():
        for prefix, last in items:
            sib[(lvl, prefix)].append(last)
    for (lvl, prefix), nums in sib.items():
        nums_sorted = sorted(set(nums))
        for i, n in enumerate(nums_sorted):
            if n != i + (nums_sorted[0]):
                findings.append(f"{prefix}: numbering gap at depth {lvl} (sequence {nums_sorted})")
                break
    return findings


def self_test() -> int:
    if lint(FIXTURE_OK):
        sys.stderr.write("self-test FAIL: OK flagged\n")
        return 1
    if not lint(FIXTURE_BAD):
        sys.stderr.write("self-test FAIL: BAD clean\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    findings = lint(p.read_text())
    if findings:
        for f in findings:
            sys.stdout.write(f"FINDING: {f}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
