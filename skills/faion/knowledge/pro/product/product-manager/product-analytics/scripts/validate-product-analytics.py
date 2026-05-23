#!/usr/bin/env python3
"""validate-product-analytics.py

Validate the artefact produced by the product-analytics methodology against the JSON
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

REQUIRED = ['plan_version', 'events', 'metric_tree', 'anomaly_rules', 'pii_policy']
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
    if not _re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', obj.get('plan_version') or ''):
        errs.append('plan_version must be semver')
    for e in obj.get('events') or []:
        if not _re.match(r'^[a-z][a-z0-9_]+_[a-z][a-z0-9_]+$', e.get('name') or ''):
            errs.append(f'event name {e.get("name")!r} must be object_action snake_case')
        if not e.get('owner'):
            errs.append(f'event {e.get("name")!r} missing owner')
        if e.get('status') not in ('live', 'deprecated', 'proposed'):
            errs.append(f'event {e.get("name")!r} status invalid')
    mt = obj.get('metric_tree') or {}
    if not mt.get('north_star'):
        errs.append('metric_tree.north_star missing')
    if not (2 <= len(mt.get('inputs') or []) <= 3):
        errs.append('metric_tree.inputs must have 2-3 entries')
    if not (obj.get('anomaly_rules') or []):
        errs.append('anomaly_rules empty')
    pp = obj.get('pii_policy') or {}
    if not pp.get('redact_at_ingest'):
        errs.append('pii_policy.redact_at_ingest must be true')
    return errs


GOOD = {'plan_version': '2.4.0', 'events': [{'name': 'checkout_started', 'properties': {}, 'owner': 'growth', 'status': 'live'}], 'metric_tree': {'north_star': 'wapu', 'inputs': [{'name': 'activation_rate', 'causes': 'wapu'}, {'name': 'retention_d30', 'causes': 'wapu'}]}, 'anomaly_rules': [{'metric': 'activation_rate', 'threshold': '>0.03'}], 'pii_policy': {'redact_at_ingest': True, 'fields': ['email']}}
BAD = {'plan_version': 'v1', 'events': [{'name': 'ButtonClick', 'properties': {}}], 'metric_tree': {'north_star': 'DAU'}, 'anomaly_rules': [], 'pii_policy': {'redact_at_ingest': False}}


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
