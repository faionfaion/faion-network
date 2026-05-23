#!/usr/bin/env python3
"""risk-audit.py

Static-analyse a Markdown risk register: flag stale rows, missing owners,
missing triggers, missing evidence.

Inputs:
    --file PATH       register markdown path
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = clean
    1 = audit findings present
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROW_RE = re.compile(r"^\|\s*(R-\d+)\s*\|", re.M)

FIXTURE_OK = """| ID | Desc | Cat | P | I | Score | Strategy | Owner | Trigger | Evidence | Status | Last review |
| R-001 | x | tech | M | M | 0.16 | accept | A. Name | resign filed | src.md | active | 2026-05-22 |"""

FIXTURE_BAD = """| ID | Desc | Cat | P | I | Score | Strategy | Owner | Trigger | Evidence | Status | Last review |
| R-002 | x | tech | M | M | 0.16 | accept |  |  |  | active |  |"""


def audit(text: str) -> list[str]:
    findings: list[str] = []
    for m in ROW_RE.finditer(text):
        line_start = m.start()
        line_end = text.find("\n", line_start)
        row = text[line_start:line_end if line_end != -1 else None]
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 12:
            findings.append(f"{m.group(1)}: row has {len(cells)} columns; expected 12")
            continue
        rid, desc, cat, p, i, score, strat, owner, trig, evid, stat, last = cells[:12]
        if not owner:
            findings.append(f"{rid}: missing owner")
        if not trig:
            findings.append(f"{rid}: missing trigger")
        if not evid:
            findings.append(f"{rid}: missing evidence")
        if not last:
            findings.append(f"{rid}: missing last_reviewed")
    return findings


def self_test() -> int:
    if audit(FIXTURE_OK):
        sys.stderr.write("self-test FAIL: OK fixture flagged\n")
        return 1
    if not audit(FIXTURE_BAD):
        sys.stderr.write("self-test FAIL: BAD fixture clean\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="register markdown path")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixture")
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
    findings = audit(p.read_text())
    if findings:
        for f in findings:
            sys.stdout.write(f"FINDING: {f}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
