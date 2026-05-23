#!/usr/bin/env python3
"""validate-agency-pipeline-hygiene-15min.py

Validate the artefact produced for the agency-pipeline-hygiene-15min methodology against the schema
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

REQUIRED = ['date', 'checks', 'ledger_entry']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"date": "2026-05-22", "checks": [{"item": "fields_complete", "status": "green", "action": ""}, {"item": "stage_moves_recorded", "status": "green", "action": ""}, {"item": "hot_opp_next_step", "status": "amber", "action": "Call BCorp Tue 10am"}, {"item": "loss_reasons_tagged", "status": "green", "action": ""}, {"item": "sources_tagged", "status": "green", "action": ""}], "ledger_entry": {"open_opps": 12, "hot_opps": 3, "stuck_over_30d": 1, "closed_won": 1, "closed_lost": 2, "avg_sales_cycle_days": 38}}')
BAD = json.loads('{"date": "2026-05-22", "checks": []}')


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
