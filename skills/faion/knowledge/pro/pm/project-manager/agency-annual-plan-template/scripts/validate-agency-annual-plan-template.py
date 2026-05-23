#!/usr/bin/env python3
"""validate-agency-annual-plan-template.py

Validate the artefact produced for the agency-annual-plan-template methodology against the schema
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

REQUIRED = ['agency', 'year', 'revenue_targets', 'utilisation_target', 'milestones', 'investment_lines']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"agency": "Acme Studio", "year": 2026, "revenue_targets": [{"quarter": "Q1", "project": 60000, "retainer": 30000, "productised": 5000}, {"quarter": "Q2", "project": 65000, "retainer": 35000, "productised": 8000}, {"quarter": "Q3", "project": 70000, "retainer": 35000, "productised": 12000}, {"quarter": "Q4", "project": 75000, "retainer": 40000, "productised": 15000}], "utilisation_target": 0.7, "milestones": [{"quarter": "Q2", "milestone": "Launch productised offer A", "owner": "Iryna"}], "investment_lines": [{"name": "Productised offer engineering", "cap_usd": 8000, "expected_return": "$5k MRR by Q4"}]}')
BAD = json.loads('{"agency": "x", "year": 2026, "revenue_targets": [], "utilisation_target": 0.7}')


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
