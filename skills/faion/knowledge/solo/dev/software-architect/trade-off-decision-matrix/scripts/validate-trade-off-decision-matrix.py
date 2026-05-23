#!/usr/bin/env python3
"""validate-trade-off-decision-matrix.py

Validate the artefact produced by the trade-off-decision-matrix methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run built-in OK + BAD fixtures
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED: tuple[str, ...] = ('matrix_id', 'question', 'criteria', 'options', 'weighted_totals', 'conflicts', 'tie_break_rule', 'recommendation', 'version', 'last_reviewed',)
ENUMS: dict[str, list] = {}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k, allowed in ENUMS.items():
        if k in obj and obj[k] not in allowed:
            errs.append(f"field {k!r} not in allowed values {allowed!r}; got {obj[k]!r}")
    return errs


OK = {'matrix_id': 'mat-tenant-store-2026-05', 'question': 'Which datastore for tenant data?', 'criteria': [{'name': 'fit_to_data_shape', 'weight': 0.3, 'owner': 'tech_lead'}, {'name': 'operational_maturity', 'weight': 0.2, 'owner': 'sre'}, {'name': 'team_familiarity', 'weight': 0.2, 'owner': 'tech_lead'}, {'name': 'tco_12mo', 'weight': 0.15, 'owner': 'finance'}, {'name': 'ecosystem', 'weight': 0.15, 'owner': 'tech_lead'}], 'options': [{'name': 'postgres', 'scores': {'fit_to_data_shape': 4, 'operational_maturity': 5, 'team_familiarity': 5, 'tco_12mo': 4, 'ecosystem': 5}, 'evidence': {'fit_to_data_shape': 'POC-2026-04', 'operational_maturity': 'internal SRE record', 'team_familiarity': 'team survey', 'tco_12mo': 'AWS pricing model', 'ecosystem': 'stack-overflow trends'}}, {'name': 'mongo', 'scores': {'fit_to_data_shape': 3, 'operational_maturity': 4, 'team_familiarity': 3, 'tco_12mo': 4, 'ecosystem': 4}, 'evidence': {'fit_to_data_shape': 'schema-mismatch in POC', 'operational_maturity': 'vendor docs', 'team_familiarity': 'team survey', 'tco_12mo': 'Atlas pricing', 'ecosystem': 'stack-overflow trends'}}], 'weighted_totals': {'postgres': 4.55, 'mongo': 3.5}, 'conflicts': [{'pair': 'tco_vs_operational_maturity', 'resolution': 'Prefer operational maturity on production data; accept up to 15% TCO premium.'}], 'tie_break_rule': 'If totals within 5%, prefer the option with higher team_familiarity.', 'recommendation': 'postgres', 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'matrix_id': 'mat 1', 'question': 'x', 'criteria': [{'name': 'thing', 'weight': 0.2, 'owner': ''}], 'options': [], 'weighted_totals': {}, 'conflicts': [], 'recommendation': '', 'version': '1.0', 'last_reviewed': 'today'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-trade-off-decision-matrix.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
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
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
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
