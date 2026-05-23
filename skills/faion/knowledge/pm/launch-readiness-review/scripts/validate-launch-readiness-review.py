#!/usr/bin/env python3
"""validate-launch-readiness-review.py

Validate the artefact produced by the launch-readiness-review methodology against the JSON
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

REQUIRED = ['launch_id', 'launch_date', 'gates', 'decision', 'snapshots']
ENUMS = {'decision': ['go', 'go-with-conditions', 'no-go']}


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
    GATES = ['security', 'performance', 'observability', 'runbooks', 'on_call', 'legal', 'support_enablement', 'comms_tree']
    gates = obj.get('gates') or {}
    for g in GATES:
        if g not in gates:
            errs.append(f'gates missing key: {g}')
            continue
        info = gates[g] or {}
        if not info.get('owner'):
            errs.append(f'gate {g!r} has no named owner')
        if info.get('status') not in ('green', 'yellow', 'red'):
            errs.append(f'gate {g!r} status invalid: {info.get("status")!r}')
        crit = info.get('criterion') or ''
        if len(crit) < 10:
            errs.append(f'gate {g!r} criterion too short')
    if obj.get('decision') == 'go':
        if any((gates.get(g) or {}).get('status') == 'red' for g in GATES):
            errs.append('decision=go incompatible with any red gate')
    snaps = obj.get('snapshots') or []
    if len(snaps) < 3:
        errs.append(f'snapshots need >= 3 entries (T-7, T-3, T-1); got {len(snaps)}')
    return errs


GOOD = {'launch_id': 'acme-cards-v1', 'launch_date': '2026-06-04', 'gates': {'security': {'owner': 'o-security', 'status': 'green', 'criterion': 'criterion documented per gate-criteria.yaml'}, 'performance': {'owner': 'o-performance', 'status': 'green', 'criterion': 'criterion documented per gate-criteria.yaml'}, 'observability': {'owner': 'o-observability', 'status': 'green', 'criterion': 'criterion documented per gate-criteria.yaml'}, 'runbooks': {'owner': 'o-runbooks', 'status': 'green', 'criterion': 'criterion documented per gate-criteria.yaml'}, 'on_call': {'owner': 'o-on_call', 'status': 'green', 'criterion': 'criterion documented per gate-criteria.yaml'}, 'legal': {'owner': 'o-legal', 'status': 'green', 'criterion': 'criterion documented per gate-criteria.yaml'}, 'support_enablement': {'owner': 'o-support_enablement', 'status': 'green', 'criterion': 'criterion documented per gate-criteria.yaml'}, 'comms_tree': {'owner': 'o-comms_tree', 'status': 'green', 'criterion': 'criterion documented per gate-criteria.yaml'}}, 'decision': 'go', 'snapshots': [{'t_minus_days': 7}, {'t_minus_days': 3}, {'t_minus_days': 1}]}
BAD = {'launch_id': 'L1', 'launch_date': 'soon', 'gates': {'security': {'owner': '', 'status': 'ok', 'criterion': 'ok'}}, 'decision': 'ship', 'snapshots': []}


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
