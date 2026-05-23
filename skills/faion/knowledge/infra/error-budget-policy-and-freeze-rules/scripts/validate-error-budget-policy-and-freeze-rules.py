#!/usr/bin/env python3
"""validate-error-budget-policy-and-freeze-rules.py

Validate an artefact produced by the Error Budget Policy and Freeze Rules methodology
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

REQUIRED = ['authorised_declarers', 'comms_channels', 'doctrine_url', 'freeze_allow_list', 'freeze_deny_list', 'policy_version', 'revert_criteria', 'review_date', 'signoff']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'policy_version': '1.0.0', 'doctrine_url': 'wiki/policies/error-budget.md', 'authorised_declarers': ['sre-on-call', 'service-owner', 'engineering-leader'], 'freeze_allow_list': ['security_patch', 'rollback', 'tier0_bugfix'], 'freeze_deny_list': ['new_feature', 'experiment', 'non_safety_capacity_change'], 'revert_criteria': {'budget_remaining_min_pct': 20, 'burn_rate_max': 1.0, 'duration_h': 24}, 'comms_channels': ['#incident', 'product-leadership@acme'], 'review_date': '2026-05-01', 'signoff': {'engineering_leader': 'Alice', 'product_vp': 'Bob', 'date': '2026-04-30'}}
BAD = {'policy_version': '1.0.0', 'doctrine_url': '', 'authorised_declarers': [], 'freeze_allow_list': [], 'revert_criteria': {}, 'signoff': None}


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
