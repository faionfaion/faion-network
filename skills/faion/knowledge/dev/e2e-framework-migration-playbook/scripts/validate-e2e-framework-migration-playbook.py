#!/usr/bin/env python3
"""validate-e2e-framework-migration-playbook.py

Validate the artefact for the e2e-framework-migration-playbook methodology against the JSON Schema
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

REQUIRED = ["migration_id", "wave", "entry_criteria_met", "exit_criteria_met", "modules_in_wave", "rollback_documented"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'wave' in obj and (not isinstance(obj['wave'], int) or obj['wave'] < 1 or obj['wave'] > 4):
        errs.append('wave must be int in [1,4]')
    if 'modules_in_wave' in obj and (not isinstance(obj['modules_in_wave'], int) or obj['modules_in_wave'] < 1):
        errs.append('modules_in_wave must be int >= 1')
    if 'migration_id' in obj and (not isinstance(obj['migration_id'], str) or len(obj['migration_id']) < 3):
        errs.append('migration_id must be >= 3 chars')
    for b in ('entry_criteria_met', 'exit_criteria_met', 'rollback_documented'):
        if b in obj and not isinstance(obj[b], bool):
            errs.append(b + ' must be boolean')
    return errs


OK = {'migration_id': 'cypress-to-playwright-2026q2', 'wave': 2, 'entry_criteria_met': True, 'exit_criteria_met': False, 'modules_in_wave': 18, 'rollback_documented': True, 'parity_tests_passing': 12, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'migration_id': 'x', 'wave': 5, 'modules_in_wave': 0}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
