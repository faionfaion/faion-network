#!/usr/bin/env python3
"""validate-product-lifecycle.py

Validate the artefact produced by the product-lifecycle methodology against the JSON
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

REQUIRED = ['product_id', 'as_of', 'signals', 'stage', 'investment_strategy', 'transition_memo']
ENUMS = {'stage': ['introduction', 'growth', 'maturity', 'decline']}


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
    for k in ('yoy_growth', 'monthly_churn', 'nps', 'market_share'):
        if (obj.get('signals') or {}).get(k) is None:
            errs.append(f'signals.{k} missing')
    if obj.get('stage') == 'decline' and not obj.get('sunset_plan_link'):
        errs.append('stage=decline requires sunset_plan_link')
    if len((obj.get('investment_strategy') or '')) < 20:
        errs.append('investment_strategy too short')
    if len((obj.get('transition_memo') or '')) < 20:
        errs.append('transition_memo too short')
    return errs


GOOD = {'product_id': 'p1', 'as_of': '2026-05-23', 'signals': {'yoy_growth': 0.08, 'monthly_churn': 0.015, 'nps': 42, 'market_share': 0.18}, 'stage': 'maturity', 'investment_strategy': 'Retention + efficiency: invest in NPS-moving fixes and CAC reduction.', 'transition_memo': 'Growth->Maturity: YoY 30%->8%; churn stable; reallocate to retention.', 'sunset_plan_link': None}
BAD = {'product_id': 'p1', 'as_of': 'today', 'signals': {'yoy_growth': 0.5}, 'stage': 'old', 'investment_strategy': 'ok', 'transition_memo': 'tbd'}


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
