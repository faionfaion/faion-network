#!/usr/bin/env python3
"""validate-product-led-growth.py

Validate the artefact produced by the product-led-growth methodology against the JSON
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

REQUIRED = ['product_id', 'aha_moment', 'pql_criteria', 'activation_cohort_tracked', 'expansion_owner', 'experiment_throttle']
ENUMS = {'expansion_owner': ['pm', 'growth-pm', 'pmm']}


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
    ah = obj.get('aha_moment') or {}
    mins = ah.get('max_minutes_from_signup')
    if not isinstance(mins, int) or not (1 <= mins <= 10):
        errs.append('aha_moment.max_minutes_from_signup must be 1..10')
    if not (ah.get('event_sequence') or []):
        errs.append('aha_moment.event_sequence empty')
    pql = obj.get('pql_criteria') or {}
    for k in ('events', 'frequency', 'account_shape'):
        if not pql.get(k):
            errs.append(f'pql_criteria.{k} missing')
    if not obj.get('activation_cohort_tracked'):
        errs.append('activation_cohort_tracked must be true')
    th = obj.get('experiment_throttle') or {}
    if (th.get('max_concurrent_per_step') or 99) > 2:
        errs.append('experiment_throttle.max_concurrent_per_step > 2')
    return errs


GOOD = {'product_id': 'acme-api', 'aha_moment': {'event_sequence': ['api_key_created', 'api_call_succeeded'], 'max_minutes_from_signup': 8}, 'pql_criteria': {'events': ['api_call_succeeded'], 'frequency': '>=10/week', 'account_shape': 'company_size > 10'}, 'activation_cohort_tracked': True, 'expansion_owner': 'pm', 'experiment_throttle': {'max_concurrent_per_step': 2}}
BAD = {'product_id': 'p1', 'aha_moment': {'event_sequence': [], 'max_minutes_from_signup': 30}, 'pql_criteria': {'events': []}, 'activation_cohort_tracked': False, 'expansion_owner': 'sales', 'experiment_throttle': {'max_concurrent_per_step': 5}}


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
