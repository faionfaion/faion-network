#!/usr/bin/env python3
"""validate-design-review-pr-checklist.py

Validate the artefact produced by the design-review-pr-checklist methodology against the JSON
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

REQUIRED = ['pr_id', 'reviewer', 'per_item_results', 'evidence_per_item', 'decision']
ENUMS = {'decision': ['approve', 'changes-needed', 'needs-handoff-update']}


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
    TEN_ITEMS = ['tokens', 'components', 'states', 'motion', 'accessibility', 'content_rules', 'breakpoints', 'images', 'dark_mode', 'cross_browser']
    per = obj.get('per_item_results') or {}
    ev = obj.get('evidence_per_item') or {}
    for it in TEN_ITEMS:
        if it not in per:
            errs.append(f'per_item_results missing key: {it}')
        elif per[it] not in ('pass', 'needs-changes', 'n/a-with-reason'):
            errs.append(f'per_item_results[{it!r}] invalid value: {per[it]!r}')
        elif per[it] == 'pass' and not ev.get(it):
            errs.append(f'evidence_per_item missing for passed item {it!r}')
    if obj.get('decision') == 'approve':
        if any(v == 'needs-changes' for v in per.values()):
            errs.append('decision=approve incompatible with any needs-changes per-item result')
    return errs


GOOD = {'pr_id': 'acme/web#1', 'reviewer': 'jane', 'per_item_results': {'tokens': 'pass', 'components': 'pass', 'states': 'pass', 'motion': 'pass', 'accessibility': 'pass', 'content_rules': 'pass', 'breakpoints': 'pass', 'images': 'pass', 'dark_mode': 'pass', 'cross_browser': 'pass'}, 'evidence_per_item': {'tokens': 'ok', 'components': 'ok', 'states': 'ok', 'motion': 'ok', 'accessibility': 'ok', 'content_rules': 'ok', 'breakpoints': 'ok', 'images': 'ok', 'dark_mode': 'ok', 'cross_browser': 'ok'}, 'decision': 'approve'}
BAD = {'pr_id': 'acme/web#2', 'reviewer': 'alex', 'per_item_results': {'tokens': 'pass', 'components': 'needs-changes'}, 'evidence_per_item': {}, 'decision': 'approve'}


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
