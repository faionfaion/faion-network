#!/usr/bin/env python3
"""validate-product-operations.py

Validate the artefact produced by the product-operations methodology against the JSON
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

REQUIRED = ['contract_id', 'raci', 'canonical_store_map', 'escalation_path']
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
    raci = obj.get('raci') or {}
    for a in ('tracking_plan', 'okr_cascade', 'voice_of_customer', 'launch_readiness'):
        if a not in raci:
            errs.append(f'raci missing artefact: {a}')
            continue
        for k in ('responsible', 'accountable', 'consulted', 'informed'):
            if k not in raci[a]:
                errs.append(f'raci[{a!r}] missing key: {k}')
    if not (obj.get('canonical_store_map') or []):
        errs.append('canonical_store_map empty')
    if not (obj.get('escalation_path') or []):
        errs.append('escalation_path empty')
    return errs


GOOD = {'contract_id': 'c1', 'raci': {'tracking_plan': {'responsible': 'x', 'accountable': 'y', 'consulted': ['z'], 'informed': ['w']}, 'okr_cascade': {'responsible': 'x', 'accountable': 'y', 'consulted': ['z'], 'informed': ['w']}, 'voice_of_customer': {'responsible': 'x', 'accountable': 'y', 'consulted': ['z'], 'informed': ['w']}, 'launch_readiness': {'responsible': 'x', 'accountable': 'y', 'consulted': ['z'], 'informed': ['w']}}, 'canonical_store_map': [{'artefact': 'tp', 'owner': 'po', 'link': 'x'}], 'escalation_path': [{'trigger': 'dispute', 'escalate_to': 'head'}]}
BAD = {'contract_id': 'c1', 'raci': {'tracking_plan': {'responsible': 'pm'}}, 'canonical_store_map': [], 'escalation_path': []}


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
