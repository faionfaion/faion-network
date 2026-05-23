#!/usr/bin/env python3
"""validate-agile-ceremonies-setup.py

Validate the artefact produced for the agile-ceremonies-setup methodology against the schema
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

REQUIRED = ['team', 'sprint_length_weeks', 'ceremonies', 'overhead_pct']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"team": "platform", "sprint_length_weeks": 2, "ceremonies": [{"name": "sprint_planning", "purpose": "Commit to sprint goal + ordered backlog", "timebox_minutes": 120, "attendees_mandatory": ["team", "PO"], "owner": "SM", "output": "sprint plan artefact"}, {"name": "daily_standup", "purpose": "Surface blockers + alignment", "timebox_minutes": 15, "attendees_mandatory": ["team"], "owner": "SM", "output": "blocker list"}, {"name": "review", "purpose": "Inspect increment with stakeholders", "timebox_minutes": 60, "attendees_mandatory": ["team", "PO", "stakeholders"], "owner": "PO", "output": "feedback log"}, {"name": "retro", "purpose": "Adapt team process; produce action items", "timebox_minutes": 90, "attendees_mandatory": ["team", "SM"], "owner": "SM", "output": "action items with owner+due"}], "overhead_pct": 0.08}')
BAD = json.loads('{"team": "x"}')


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
