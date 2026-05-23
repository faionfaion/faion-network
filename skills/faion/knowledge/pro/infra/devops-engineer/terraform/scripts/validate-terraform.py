#!/usr/bin/env python3
"""validate-terraform.py

Validate an artefact produced by the Terraform methodology
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

REQUIRED = ['apply_via_ci_only', 'backend', 'drift_schedule', 'modules_used', 'provider_pins', 'sensitive_marks_audited', 'state_locking', 'terraform_version']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'terraform_version': '1.7.5', 'provider_pins': {'aws': '= 5.40.0', 'random': '= 3.6.0'}, 'backend': {'type': 's3', 'config': {'bucket': 'acme-tfstate', 'dynamodb_table': 'acme-tflock'}}, 'state_locking': True, 'apply_via_ci_only': True, 'modules_used': [{'source': 'registry.acme/vpc', 'version': '2.1.0'}], 'sensitive_marks_audited': True, 'drift_schedule': '0 8 * * MON'}
BAD = {'terraform_version': 'latest', 'provider_pins': {}, 'backend': {'type': 'local'}, 'state_locking': False, 'apply_via_ci_only': False}


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
