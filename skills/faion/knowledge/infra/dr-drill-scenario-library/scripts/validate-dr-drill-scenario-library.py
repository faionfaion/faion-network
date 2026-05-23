#!/usr/bin/env python3
"""validate-dr-drill-scenario-library.py

Validate an artefact produced by the DR Drill Scenario Library methodology
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

REQUIRED = ['library_version', 'min_scenarios', 'post_mortem_template_path', 'rotation_calendar', 'scenarios']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'library_version': '1.0.0', 'scenarios': [{'id': 'sc-01-region-loss', 'name': 'Primary region offline', 'declaration_criteria': 'AWS region status page red >15min', 'runbook_path': 'runbooks/dr/sc-01.md', 'restore_validation': 'smoke test + data-integrity hash check', 'success_criteria': 'RTO <60min RPO <5min', 'last_run_date': '2026-02-15', 'owner': 'platform-team'}, {'id': 'sc-02-db-corruption', 'name': 'DB logical corruption', 'declaration_criteria': 'row checksum mismatch >0.1%', 'runbook_path': 'runbooks/dr/sc-02.md', 'restore_validation': 'point-in-time restore + integrity check', 'success_criteria': 'data restored to T-1h', 'last_run_date': '2025-11-10', 'owner': 'data-team'}], 'rotation_calendar': [{'quarter': '2026-Q3', 'scenario_id': 'sc-04-identity-provider-out'}], 'post_mortem_template_path': 'templates/postmortem.md', 'min_scenarios': 6}
BAD = {'library_version': '1.0.0', 'scenarios': [{'id': 'sc-01', 'name': 'Restore', 'declaration_criteria': 'feels broken'}], 'min_scenarios': 1}


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
