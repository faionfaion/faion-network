#!/usr/bin/env python3
"""validate-minimum-product-frameworks.py

Validate the artefact produced by the minimum-product-frameworks methodology against the JSON
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

REQUIRED = ['dr_id', 'signals', 'selected_framework', 'scorecard', 'differentiator_proof', 'revisit_triggers']
ENUMS = {'selected_framework': ['MVP', 'MLP', 'MMP', 'MAC', 'RAT', 'MDP', 'MVA', 'MFP', 'SLC']}


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
    if not _re.match(r'^dr-[a-z0-9-]+-[0-9]{4}-[0-9]{2}-[0-9]{2}$', obj.get('dr_id') or ''):
        errs.append('dr_id must match dr-<slug>-YYYY-MM-DD pattern')
    sc = obj.get('scorecard') or {}
    for f in ('MVP', 'MLP', 'MMP', 'MAC', 'RAT', 'MDP', 'MVA', 'MFP', 'SLC'):
        if f not in sc:
            errs.append(f'scorecard missing framework: {f}')
        elif not (0 <= sc[f] <= 5):
            errs.append(f'scorecard[{f}] out of [0,5]: {sc[f]}')
    if len((obj.get('differentiator_proof') or '')) < 15:
        errs.append('differentiator_proof too short (>= 15 chars required)')
    trig = obj.get('revisit_triggers') or []
    if len(trig) < 2:
        errs.append(f'revisit_triggers need >= 2 entries (got {len(trig)})')
    return errs


GOOD = {'dr_id': 'dr-acme-cards-2026-05-23', 'signals': {'market_density': 'blue-ocean', 'buyer_type': 'prosumer', 'differentiator': 'experience'}, 'selected_framework': 'MLP', 'scorecard': {'MVP': 3, 'MLP': 5, 'MMP': 3, 'MAC': 2, 'RAT': 2, 'MDP': 1, 'MVA': 1, 'MFP': 1, 'SLC': 4}, 'differentiator_proof': 'Day-30 retention >= 45% and NPS >= 40 within 60 days of GA.', 'revisit_triggers': ['Day-30 retention < 25% for 2 cohorts.', 'NPS < 20 in wave-2 survey.']}
BAD = {'dr_id': 'DR1', 'signals': {'market_density': '??', 'buyer_type': '?', 'differentiator': '?'}, 'selected_framework': 'agile', 'scorecard': {'MVP': 99}, 'differentiator_proof': 'tbd', 'revisit_triggers': ['?']}


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
