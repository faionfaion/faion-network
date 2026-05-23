#!/usr/bin/env python3
"""validate-mlp-planning.py

Validate the artefact produced by the mlp-planning methodology against the JSON
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

REQUIRED = ['plan_id', 'layer_scores', 'delight_backlog', 'retention_curve_target', 'sprint_plan']
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
    ls = obj.get('layer_scores') or {}
    for layer in ('functional', 'reliable', 'usable', 'delightful'):
        if layer not in ls:
            errs.append(f'layer_scores missing: {layer}')
            continue
        s = (ls[layer] or {}).get('score')
        if not isinstance(s, int) or not (0 <= s <= 5):
            errs.append(f'layer_scores.{layer}.score must be int 0..5')
    f = (ls.get('functional') or {}).get('score') or 0
    r = (ls.get('reliable') or {}).get('score') or 0
    d = (ls.get('delightful') or {}).get('score') or 0
    if (f < 3 or r < 3) and d >= 3:
        errs.append('delightful >=3 with broken base; apply delight-only-when-base-ge-3 rule')
    for it in obj.get('delight_backlog') or []:
        if not (it.get('quotes') or []):
            errs.append(f'delight item {it.get("id")!r} has no quotes (designer-opinion)')
    rt = obj.get('retention_curve_target') or {}
    if not (0 <= (rt.get('baseline_d30') or -1) <= 1):
        errs.append('baseline_d30 outside [0,1]')
    if not (0 <= (rt.get('target_d30') or -1) <= 1):
        errs.append('target_d30 outside [0,1]')
    for sp in obj.get('sprint_plan') or []:
        if (sp.get('duration_days') or 0) > 14:
            errs.append('sprint duration_days > 14 (unbounded)')
    return errs


GOOD = {'plan_id': 'mlp-1', 'layer_scores': {'functional': {'score': 4, 'evidence': 'core flow ok'}, 'reliable': {'score': 4, 'evidence': 'p95 ok'}, 'usable': {'score': 3, 'evidence': 'SUS 68'}, 'delightful': {'score': 2, 'evidence': 'NPS 22'}}, 'delight_backlog': [{'id': 'd1', 'theme': 'onboarding', 'quotes': [{'participant_id': 'U_1', 'verbatim': 'feel like winning'}]}], 'retention_curve_target': {'baseline_d30': 0.22, 'target_d30': 0.38, 'window_weeks': 8}, 'sprint_plan': [{'theme': 'onboarding', 'duration_days': 10}]}
BAD = {'plan_id': 'P1', 'layer_scores': {'functional': {'score': 2}, 'delightful': {'score': 5}}, 'delight_backlog': [{'id': 'x', 'theme': 'polish', 'quotes': []}], 'retention_curve_target': {'baseline_d30': 1.5, 'target_d30': 0.1, 'window_weeks': 100}, 'sprint_plan': [{'theme': 'everything', 'duration_days': 60}]}


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
