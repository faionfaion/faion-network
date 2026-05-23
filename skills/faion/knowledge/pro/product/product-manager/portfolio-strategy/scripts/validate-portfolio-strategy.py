#!/usr/bin/env python3
"""validate-portfolio-strategy.py

Validate the artefact produced by the portfolio-strategy methodology against the JSON
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

REQUIRED = ['quarter', 'products', 'allocation', 'kill_triggers', 'rebalance_memo_link']
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
    import re as _re
    if not _re.match(r'^[0-9]{4}-Q[1-4]$', obj.get('quarter') or ''):
        errs.append('quarter must match YYYY-QX')
    prods = obj.get('products') or []
    if len(prods) < 2:
        errs.append('products need >= 2 entries')
    for p in prods:
        if p.get('horizon') not in ('H1', 'H2', 'H3'):
            errs.append(f'product {p.get("id")!r} horizon must be H1/H2/H3')
    alloc = obj.get('allocation') or {}
    for k in ('h1_pct', 'h2_pct', 'h3_pct'):
        v = alloc.get(k)
        if not isinstance(v, (int, float)) or not (0 <= v <= 100):
            errs.append(f'allocation.{k} must be 0..100')
    kt = obj.get('kill_triggers') or {}
    for h in ('H1', 'H2', 'H3'):
        if not (kt.get(h) or []):
            errs.append(f'kill_triggers.{h} missing or empty')
    return errs


GOOD = {'quarter': '2026-Q2', 'products': [{'id': 'p1', 'horizon': 'H1', 'rationale': 'core mature', 'capacity_pct': 65}, {'id': 'p2', 'horizon': 'H2', 'rationale': 'adjacent 8mo in', 'capacity_pct': 22}, {'id': 'p3', 'horizon': 'H3', 'rationale': 'transformational y1', 'capacity_pct': 13}], 'allocation': {'h1_pct': 65, 'h2_pct': 22, 'h3_pct': 13}, 'kill_triggers': {'H1': ['retention slip'], 'H2': ['18mo no PMF'], 'H3': ['36mo no signal']}, 'rebalance_memo_link': 'memo-2026-q2.md'}
BAD = {'quarter': '2026', 'products': [{'id': 'p1', 'horizon': 'X', 'rationale': ''}], 'allocation': {'h1_pct': 100, 'h2_pct': 0, 'h3_pct': 0}, 'kill_triggers': {'H1': []}}


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
