#!/usr/bin/env python3
"""validate-dr-drill-script-template.py

Validate an artefact produced by the DR Drill Script Template methodology
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

REQUIRED = ['declaration_time', 'drill_id', 'gap_tickets', 'gaps_found', 'post_mortem_published_date', 'post_mortem_url', 'restore_time', 'rpo_achieved_minutes', 'rpo_target_minutes', 'rto_achieved_minutes', 'rto_target_minutes', 'runbook_deviations', 'scenario_id', 'validation_pass']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'drill_id': '2026-Q3-sc-04', 'scenario_id': 'sc-04-identity-provider-out', 'declaration_time': '2026-08-15T14:22:00Z', 'restore_time': '2026-08-15T15:09:00Z', 'validation_pass': True, 'rto_achieved_minutes': 47, 'rpo_achieved_minutes': 0, 'rto_target_minutes': 60, 'rpo_target_minutes': 5, 'runbook_deviations': ['Step 4: secondary IdP creds rotated, used backup credentials from Vault'], 'gaps_found': ['fallback auth path lacked MFA enrollment script'], 'gap_tickets': ['INC-2026-08-15-001'], 'post_mortem_url': 'wiki/postmortems/sc-04-2026-q3.md', 'post_mortem_published_date': '2026-08-19'}
BAD = {'drill_id': '2026-Q3', 'scenario_id': 'unknown', 'declaration_time': '', 'validation_pass': False, 'rto_achieved_minutes': 999, 'post_mortem_published_date': ''}


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
