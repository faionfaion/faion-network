#!/usr/bin/env python3
"""validate-schedule-development.py

Validate the artefact produced for the schedule-development methodology against the schema
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

REQUIRED = ['project', 'baseline_date', 'last_refreshed', 'activities', 'buffers']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"project": "data-platform-q3", "baseline_date": "2026-04-01", "last_refreshed": "2026-05-22", "activities": [{"id": "A01", "name": "Design data model", "wbs_pkg": "1.2", "predecessors": [], "estimate": {"mode": "pert", "o": 2, "m": 3, "p": 5, "pert_days": 3.2}, "resource": "team A"}, {"id": "A02", "name": "Implement ingest pipeline", "wbs_pkg": "1.3", "predecessors": [{"id": "A01", "type": "FS"}], "estimate": {"mode": "pert", "o": 4, "m": 6, "p": 10, "pert_days": 6.3}, "resource": "team A"}], "buffers": [{"id": "PB", "type": "project", "size_days": 4.0, "chain": "critical"}]}')
BAD = json.loads('{"project": "x", "activities": [{"id": "a1", "name": "stuff"}]}')


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
