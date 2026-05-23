#!/usr/bin/env python3
"""validate-project-closure-with-lessons-extraction.py

Validate the artefact produced for the project-closure-with-lessons-extraction methodology against the schema
in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['project', 'sponsor', 'outcome', 'charter_goal', 'actual_outcome', 'variance_reason', 'lessons', 'decisions_next_project', 'open_items']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"project": "phoenix-rescue", "sponsor": "VP Engineering", "outcome": "partial", "charter_goal": "Stabilise checkout p95 latency below 500ms within 90 days.", "actual_outcome": "p95 latency 540ms at day 90; 8% above target.", "variance_reason": "Underestimated vendor migration window by 3 weeks.", "lessons": [{"id": "L-001", "statement": "Vendor migrations consistently underestimated.", "behaviour_change": "Add vendor-migration buffer of 1.5x to PERT estimates for any vendor change.", "owner": "PM Iryna", "target_adoption_date": "2026-07-15", "evidence": "phoenix-postmortem-section-4.md"}], "decisions_next_project": [{"statement": "Pin vendor SOW v3 before kickoff"}], "open_items": [{"item": "Document Stripe v2 quirks", "owner": "Petro", "due": "2026-06-30"}]}')
BAD = json.loads('{"project": "x", "outcome": "great"}')


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: OK fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
