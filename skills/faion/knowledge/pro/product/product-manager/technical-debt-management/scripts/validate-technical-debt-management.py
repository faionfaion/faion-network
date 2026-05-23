#!/usr/bin/env python3
"""validate-technical-debt-management.py

Validate the artefact produced by the technical-debt-management methodology against the JSON
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

REQUIRED = ['register_id', 'items', 'capacity_contract', 'visibility']
ENUMS = {'visibility': ['public-to-stakeholders', 'engineering-private']}


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
    import re as _re
    TYPES = {'design', 'code', 'test', 'infra', 'docs', 'dependency'}
    for it in obj.get('items') or []:
        if it.get('type') not in TYPES:
            errs.append(f'item {it.get("id")!r} type invalid')
        if (it.get('paydown_effort_days') or 0) <= 0:
            errs.append(f'item {it.get("id")!r} paydown_effort_days must be > 0')
        if len((it.get('prevention_policy') or '')) < 10:
            errs.append(f'item {it.get("id")!r} prevention_policy too short')
    cc = obj.get('capacity_contract') or {}
    if not _re.match(r'^[0-9]{4}-Q[1-4]$', cc.get('quarter') or ''):
        errs.append('capacity_contract.quarter must be YYYY-QX')
    p = cc.get('percent_of_sprint')
    if not isinstance(p, (int, float)) or not (5 <= p <= 30):
        errs.append(f'capacity_contract.percent_of_sprint must be 5..30 (got {p})')
    if len(cc.get('agreed_by') or []) < 2:
        errs.append('capacity_contract.agreed_by needs >=2 signatories')
    if obj.get('visibility') == 'engineering-private':
        errs.append('visibility must be public-to-stakeholders (rule debt-visibility-public)')
    return errs


GOOD = {'register_id': 'r1', 'items': [{'id': 'd1', 'type': 'code', 'interest_per_month': 12.0, 'contagion_factor': 1.6, 'paydown_effort_days': 8.0, 'prevention_policy': 'ruff rule + CI gate'}], 'capacity_contract': {'quarter': '2026-Q2', 'percent_of_sprint': 18, 'agreed_by': ['pm', 'tech-lead']}, 'visibility': 'public-to-stakeholders'}
BAD = {'register_id': 'r1', 'items': [{'id': 'x', 'type': 'stuff', 'interest_per_month': -1, 'contagion_factor': -1, 'paydown_effort_days': 0, 'prevention_policy': 'tbd'}], 'capacity_contract': {'quarter': '2026', 'percent_of_sprint': 50, 'agreed_by': ['pm']}, 'visibility': 'secret'}


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
