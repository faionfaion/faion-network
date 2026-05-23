#!/usr/bin/env python3
"""validate-release-planning.py

Validate the artefact produced by the release-planning methodology against the JSON
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

REQUIRED = ['release_id', 'cadence', 'release_date', 'readiness_matrix', 'deprecations', 'post_release_monitor']
ENUMS = {'cadence': ['weekly', 'biweekly', 'monthly']}


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
    from datetime import date as _date
    FUNCS = ['engineering', 'qa', 'support', 'sales', 'marketing', 'legal']
    rm = obj.get('readiness_matrix') or {}
    for f in FUNCS:
        if f not in rm:
            errs.append(f'readiness_matrix missing: {f}')
            continue
        info = rm[f] or {}
        if info.get('status') not in ('green', 'yellow', 'red'):
            errs.append(f'readiness_matrix[{f}].status invalid')
        if not info.get('owner'):
            errs.append(f'readiness_matrix[{f}].owner empty')
    for d in obj.get('deprecations') or []:
        try:
            rd = _date.fromisoformat(d.get('removal_date'))
            fa = _date.fromisoformat(d.get('first_announced'))
            if (rd - fa).days < 90:
                errs.append(f'deprecation {d.get("item")!r} notice < 90 days')
        except Exception:
            errs.append(f'deprecation {d.get("item")!r}: bad dates')
    if obj.get('release_notes_customer_facing') is False:
        errs.append('release_notes_customer_facing must be true')
    prm = obj.get('post_release_monitor') or {}
    if (prm.get('window_hours') or 0) < 24:
        errs.append('post_release_monitor.window_hours must be >= 24')
    if not prm.get('owner'):
        errs.append('post_release_monitor.owner empty')
    return errs


GOOD = {'release_id': 'r-1', 'cadence': 'biweekly', 'release_date': '2026-05-30', 'readiness_matrix': {'engineering': {'owner': 'o-engineering', 'status': 'green'}, 'qa': {'owner': 'o-qa', 'status': 'green'}, 'support': {'owner': 'o-support', 'status': 'green'}, 'sales': {'owner': 'o-sales', 'status': 'green'}, 'marketing': {'owner': 'o-marketing', 'status': 'green'}, 'legal': {'owner': 'o-legal', 'status': 'green'}}, 'deprecations': [{'item': '/v1', 'removal_date': '2026-08-30', 'first_announced': '2026-05-01', 'customer_notified': True}], 'release_notes_customer_facing': True, 'post_release_monitor': {'owner': 'oncall', 'window_hours': 24, 'rollback_triggers': ['err>1%']}}
BAD = {'release_id': 'r1', 'cadence': 'ad-hoc', 'release_date': 'soon', 'readiness_matrix': {'engineering': {'owner': 'x', 'status': 'green'}}, 'deprecations': [{'item': 'v1', 'removal_date': '2026-05-20', 'first_announced': '2026-05-01'}], 'release_notes_customer_facing': False, 'post_release_monitor': {'owner': '', 'window_hours': 0, 'rollback_triggers': []}}


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
