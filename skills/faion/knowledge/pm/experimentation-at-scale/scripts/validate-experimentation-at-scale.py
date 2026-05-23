#!/usr/bin/env python3
"""validate-experimentation-at-scale.py

Validate the artefact produced by the experimentation-at-scale methodology against the JSON
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

REQUIRED = ['experiment_id', 'hypothesis', 'primary_metric', 'guardrails', 'mde', 'decision']
ENUMS = {'decision': ['ship', 'kill', 'iterate', 'pending']}


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
    exp = obj.get('experiment_id') or ''
    if not _re.match(r'^[a-z][a-z0-9-]+$', exp):
        errs.append('experiment_id must be kebab-case')
    if len((obj.get('hypothesis') or '')) < 20:
        errs.append('hypothesis too short (need >= 20 chars)')
    gr = obj.get('guardrails') or []
    if len(gr) < 3:
        errs.append(f'guardrails must have >= 3 entries (got {len(gr)})')
    mde = obj.get('mde') or {}
    if (mde.get('sample_size') or 0) < 1 or (mde.get('runtime_days') or 0) < 1:
        errs.append('mde.sample_size and mde.runtime_days must be >= 1')
    pm = obj.get('primary_metric') or {}
    if 'delta_direction' not in pm:
        errs.append('primary_metric.delta_direction required')
    elif pm['delta_direction'] not in ('increase', 'decrease'):
        errs.append('primary_metric.delta_direction must be increase|decrease')
    if 'srm_passed' in obj and not obj['srm_passed'] and obj.get('decision') != 'kill':
        errs.append('srm_passed=false requires decision=kill')
    return errs


GOOD = {'experiment_id': 'checkout-v2-button-color', 'hypothesis': 'Changing checkout button color to high-contrast blue increases conversion', 'primary_metric': {'name': 'checkout_conversion_rate', 'delta_direction': 'increase'}, 'guardrails': [{'name': 'p95_latency_ms', 'floor': '<=250'}, {'name': 'error_rate', 'floor': '<=0.005'}, {'name': 'revenue_per_user', 'floor': '>=baseline'}], 'mde': {'effect_size': '+2pp', 'sample_size': 24000, 'runtime_days': 14}, 'srm_passed': True, 'decision': 'ship'}
BAD = {'experiment_id': 'EXP1', 'hypothesis': 'stuff', 'primary_metric': {'name': 'x'}, 'guardrails': [{'name': 'latency', 'floor': '<=250'}], 'mde': {'effect_size': '?', 'sample_size': 0, 'runtime_days': 0}, 'decision': 'hold'}


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
