#!/usr/bin/env python3
"""validate-continuous-discovery-habits.py

Validate the artefact produced by the continuous-discovery-habits methodology against the JSON
Schema in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    path to artefact JSON
    --self-test    run built-in fixtures
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['tree_version', 'outcome', 'opportunities', 'weekly_readout']
ENUMS = {}


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    for field, allowed in ENUMS.items():
        v = obj.get(field)
        if v is not None and v not in allowed:
            errs.append(f"{field} must be one of {sorted(allowed)} (got {v!r})")
    outcome = obj.get('outcome', {})
    if not isinstance(outcome, dict) or not outcome.get('movability_check_passed'):
        errs.append('outcome.movability_check_passed must be true')
    opps = obj.get('opportunities') or []
    if not opps:
        errs.append('opportunities empty')
    for op in opps:
        if not isinstance(op, dict):
            errs.append('opportunity must be object'); continue
        if not op.get('quotes'):
            errs.append(f"opportunity {op.get('id')!r} has no quotes")
        name = (op.get('id') or '').lower()
        if name.startswith('build-') or name.startswith('add-'):
            errs.append(f"opportunity id {op.get('id')!r} is solution-shaped")
    wr = obj.get('weekly_readout') or {}
    if (wr.get('interviews') or 0) < 1:
        errs.append('weekly_readout.interviews must be >= 1')
    return errs


GOOD = {'tree_version': '2026-Q2.4', 'outcome': {'id': 'activation-rate-improved', 'movability_check_passed': True}, 'opportunities': [{'id': 'op-onboarding-friction', 'shape': 'pain', 'quotes': [{'participant_id': 'U_3471', 'interview_date': '2026-05-19', 'verbatim': 'had to scroll through six tabs.'}]}], 'weekly_readout': {'week': '2026-W21', 'interviews': 2, 'tree_diff': []}}
BAD = {'tree_version': 'draft', 'outcome': {'id': 'growth', 'movability_check_passed': False}, 'opportunities': [{'id': 'build-onboarding', 'shape': 'problem', 'quotes': []}], 'weekly_readout': {'week': '2026-21', 'interviews': 0, 'tree_diff': []}}


def self_test():
    errs_good = validate(GOOD)
    if errs_good:
        sys.stderr.write(f"GOOD rejected: {errs_good}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to artefact JSON")
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
