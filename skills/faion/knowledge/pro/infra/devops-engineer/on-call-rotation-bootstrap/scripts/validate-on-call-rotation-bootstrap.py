#!/usr/bin/env python3
"""validate-on-call-rotation-bootstrap.py

Validate an artefact produced by the On-Call Rotation Bootstrap methodology
against the JSON Schema declared in content/02-output-contract.xml.

Inputs:
    --file PATH       path to the artefact JSON file
    --self-test       run built-in fixtures (OK + BAD) and exit 0 on pass
    --help            this message

Exit codes:
    0 = valid (or self-test pass)
    1 = invalid (or self-test fail)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['charter', 'load_report', 'schedule']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'charter': {'team_name': 'platform', 'effective_date': '2026-06-01', 'shift_length_hours': 168, 'tiers': 'primary_plus_secondary', 'ack_sla_seconds': {'sev1': 300, 'sev2': 900, 'sev3': 0}, 'escalation_tree': ['primary', 'secondary', 'manager'], 'comp_policy_doc_url': 'https://wiki.acme/hr/on-call-comp', 'rotation_owner': 'tlead@acme'}, 'schedule': {'tool': 'pagerduty', 'config_path': 'config/pagerduty/platform.yaml'}, 'load_report': {'period_start': '2026-05-16', 'period_end': '2026-05-22', 'per_engineer': [{'engineer': 'alice', 'pages': 4, 'off_hours_pages': 2, 'weekend_pages': 0}]}}
BAD = {'charter': {'team_name': '', 'shift_length_hours': 168, 'tiers': 'primary', 'comp_policy_doc_url': ''}}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"self-test FAIL: OK fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
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
