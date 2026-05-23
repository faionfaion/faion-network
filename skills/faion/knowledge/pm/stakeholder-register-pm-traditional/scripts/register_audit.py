#!/usr/bin/env python3
"""register_audit.py

Audit a stakeholder register: flag rows missing evidence, attitude outside the
enum, or last_reviewed older than 30 days.

Inputs:
    --file PATH       register JSON (list of entries)
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = clean
    1 = audit findings present
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

ATTITUDE = {"champion", "supporter", "neutral", "critic", "blocker"}
STALE_DAYS = 30

FIXTURE_OK = {"as_of": "2026-05-22", "stakeholders": [
    {"id": "S-001", "name": "x", "role": "y", "power": "low", "interest": "high",
     "attitude": "supporter", "strategy": "regular brief", "evidence": "minutes.md",
     "last_reviewed": "2026-05-10"},
]}
FIXTURE_BAD = {"as_of": "2026-05-22", "stakeholders": [
    {"id": "S-001", "name": "x", "role": "y", "power": "low", "interest": "high",
     "attitude": "unknown", "strategy": "x", "evidence": "",
     "last_reviewed": "2026-01-01"},
]}


def audit(reg: dict) -> list[str]:
    as_of = datetime.strptime(reg["as_of"], "%Y-%m-%d").date()
    findings: list[str] = []
    for s in reg.get("stakeholders", []):
        sid = s.get("id", "?")
        if s.get("attitude") not in ATTITUDE:
            findings.append(f"{sid}: attitude not in enum")
        if not s.get("evidence"):
            findings.append(f"{sid}: evidence empty")
        try:
            last = datetime.strptime(s["last_reviewed"], "%Y-%m-%d").date()
            if (as_of - last).days > STALE_DAYS:
                findings.append(f"{sid}: stale ({(as_of - last).days}d > {STALE_DAYS}d)")
        except (KeyError, ValueError):
            findings.append(f"{sid}: last_reviewed missing or malformed")
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
    reg = json.loads(p.read_text())
    findings = audit(reg)
    if findings:
        for f in findings:
            sys.stdout.write(f"FINDING: {f}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
