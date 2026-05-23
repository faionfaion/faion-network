#!/usr/bin/env python3
"""validate-program-weekly-note-template.py

Validate the artefact produced for the program-weekly-note-template methodology against the schema
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

REQUIRED = ['program', 'week', 'date', 'headline', 'progress', 'risks_moved', 'decisions', 'sponsor_asks', 'last_week_outcomes']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"program": "checkout-redesign", "week": 5, "date": "2026-05-22", "headline": "On track; canary p95 holds under 500ms; vendor SOW signed.", "progress": [{"workstream": "Payments", "summary": "Stripe v2 client deployed", "evidence": "PR-412"}], "risks_moved": [{"id": "R-001", "delta_reason": "vendor SOW signed \\u2192 mitigated"}, {"id": "R-002", "delta_reason": "key dev on PTO \\u2192 escalated"}, {"id": "R-003", "delta_reason": "p95 canary holds \\u2192 closed_passed"}], "decisions": [{"statement": "Apple Pay rollout starts UA+PT", "owner": "Iryna"}], "sponsor_asks": [{"n": 1, "ask": "Approve UA+PT canary geography for Apple Pay rollout"}], "last_week_outcomes": [{"item": "Ask 1: extend vendor SOW", "status": "closed", "evidence": "signed-sow-v2.pdf"}]}')
BAD = json.loads('{"program": "x", "week": 1, "headline": ""}')


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
