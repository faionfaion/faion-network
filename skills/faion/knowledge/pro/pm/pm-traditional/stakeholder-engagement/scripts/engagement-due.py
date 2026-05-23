#!/usr/bin/env python3
"""engagement-due.py

Flag stakeholders whose last engagement is overdue per quadrant cadence.
Quadrant cadence (from 01-core-rules.xml):
    manage_closely (high-power, high-interest): weekly
    keep_satisfied (high-power, low-interest): biweekly
    keep_informed  (low-power,  high-interest): biweekly
    monitor        (low-power,  low-interest):  monthly

Inputs:
    --file PATH       stakeholder register JSON
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = no overdue stakeholders
    1 = overdue present
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DUE_DAYS = {"manage_closely": 7, "keep_satisfied": 14, "keep_informed": 14, "monitor": 30}

FIXTURE_OK = {"as_of": "2026-05-22",
              "stakeholders": [
                  {"id": "S-001", "quadrant": "manage_closely", "last_engagement": "2026-05-18"},
              ]}
FIXTURE_BAD = {"as_of": "2026-05-22",
               "stakeholders": [
                   {"id": "S-001", "quadrant": "manage_closely", "last_engagement": "2026-04-01"},
               ]}


def overdue(state: dict) -> list[str]:
    as_of = datetime.strptime(state["as_of"], "%Y-%m-%d").date()
    findings: list[str] = []
    for s in state.get("stakeholders", []):
        days = DUE_DAYS.get(s.get("quadrant", ""))
        if days is None:
            findings.append(f"{s.get('id')}: unknown quadrant")
            continue
        last = datetime.strptime(s["last_engagement"], "%Y-%m-%d").date()
        if (as_of - last).days > days:
            findings.append(f"{s['id']}: overdue ({(as_of - last).days}d > {days}d for {s['quadrant']})")
    return findings


def self_test() -> int:
    if overdue(FIXTURE_OK):
        sys.stderr.write("self-test FAIL: OK fixture flagged\n")
        return 1
    if not overdue(FIXTURE_BAD):
        sys.stderr.write("self-test FAIL: BAD fixture clean\n")
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
    state = json.loads(p.read_text())
    findings = overdue(state)
    if findings:
        for f in findings:
            sys.stdout.write(f"FINDING: {f}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
