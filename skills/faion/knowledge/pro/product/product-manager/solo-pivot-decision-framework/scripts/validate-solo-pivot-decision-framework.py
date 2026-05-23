#!/usr/bin/env python3
"""validate-solo-pivot-decision-framework.py

Validate the artefact produced by the solo-pivot-decision-framework methodology against the JSON
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

REQUIRED = ['product_id', 'as_of', 'triggers', 'pivot_type', 'sunk_costs', 'runway_weeks', 'pivot_history']
ENUMS = {'pivot_type': ['segment', 'feature', 'business-model', 'tech', 'channel'], 'decision': ['pivot', 'quit', 'persevere']}


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
    if not (obj.get('triggers') or []):
        errs.append('triggers empty (vibe-pivot)')
    if not (obj.get('sunk_costs') or []):
        errs.append('sunk_costs empty (must disclose)')
    rw = obj.get('runway_weeks') or 0
    if rw < 8:
        errs.append(f'runway_weeks {rw} < 8 (apply runway-feasibility-gate)')
    failed = sum(1 for p in (obj.get('pivot_history') or []) if (p.get('outcome') or '').lower() == 'failed')
    if failed >= 3 and obj.get('decision') == 'pivot':
        errs.append('3 prior failed pivots; rule pivot-vs-quit forces decision=quit')
    return errs


GOOD = {'product_id': 'acme-saas', 'as_of': '2026-05-23', 'triggers': [{'name': 'mrr_trailing_30d', 'value': 4200, 'threshold': 'flat 90d'}], 'pivot_type': 'segment', 'sunk_costs': [{'item': '9mo eng', 'magnitude': '1.4 FTE-yr'}], 'runway_weeks': 14, 'pivot_history': [], 'decision': 'pivot'}
BAD = {'product_id': 'p1', 'as_of': 'today', 'triggers': [], 'pivot_type': 'everything', 'sunk_costs': [], 'runway_weeks': 2, 'pivot_history': [{'date': '2024-01-01', 'type': 'segment', 'outcome': 'failed'}, {'date': '2024-05-01', 'type': 'feature', 'outcome': 'failed'}, {'date': '2024-09-01', 'type': 'tech', 'outcome': 'failed'}], 'decision': 'pivot'}


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
