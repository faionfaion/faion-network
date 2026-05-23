#!/usr/bin/env python3
"""validate-slo-burn-decision-matrix.py

Validate an artefact produced by the SLO Burn Decision Matrix methodology
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

REQUIRED = ['audit_destination', 'default_cell', 'matrix_version', 'portfolio_id', 'rows']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'matrix_version': '1.0.0', 'portfolio_id': 'acme-platform', 'rows': [{'burn_category': 'fast', 'service_class': 'user-facing-critical', 'action': 'halt-canary', 'owner': 'release-manager', 'revert_criteria': 'burn_rate<1 for 6h'}, {'burn_category': 'medium', 'service_class': 'user-facing-critical', 'action': 'freeze-ship', 'owner': 'release-manager', 'revert_criteria': 'budget>=20% remaining'}, {'burn_category': 'slow', 'service_class': 'user-facing-critical', 'action': 'focus-shift', 'owner': 'service-owner', 'revert_criteria': 'next_release'}, {'burn_category': 'fast', 'service_class': 'internal', 'action': 'accept', 'owner': 'service-owner', 'revert_criteria': 'auto'}], 'audit_destination': 'https://siem.acme/ingest/slo-matrix', 'default_cell': 'escalate'}
BAD = {'matrix_version': '1.0.0', 'portfolio_id': 'acme-platform', 'rows': [{'burn_category': 'fast', 'service_class': 'user-facing-critical', 'action': 'depends', 'owner': 'team'}], 'default_cell': 'accept'}


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
