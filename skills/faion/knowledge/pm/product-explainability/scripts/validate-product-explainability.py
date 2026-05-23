#!/usr/bin/env python3
"""validate-product-explainability.py

Validate the artefact produced by the product-explainability methodology against the JSON
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

REQUIRED = ['narrative_id', 'problem', 'who', 'behaviour_change', 'outcome_metric', 'evidence_link', 'audience_renders']
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
    for f in ('problem', 'behaviour_change'):
        if len((obj.get(f) or '')) < 15:
            errs.append(f'{f} too short (>= 15 chars required)')
    if not (obj.get('evidence_link') or ''):
        errs.append('evidence_link must be non-empty')
    om = obj.get('outcome_metric') or {}
    for k in ('metric', 'baseline', 'target'):
        if not om.get(k):
            errs.append(f'outcome_metric.{k} missing')
    ren = obj.get('audience_renders') or {}
    for a in ('exec', 'sales', 'support', 'customer'):
        if not ren.get(a):
            errs.append(f'audience_renders.{a} missing')
    bc = (obj.get('behaviour_change') or '').lower()
    if bc.startswith('we added') or bc.startswith('we built') or bc.startswith('we shipped'):
        errs.append('behaviour_change phrased as feature-shipped; rule outcome-not-feature')
    return errs


GOOD = {'narrative_id': 'checkout-redesign', 'problem': 'Users abandon checkout below the fold.', 'who': 'Mobile shoppers (smb-prosumer)', 'behaviour_change': 'Shoppers see and select preferred method without scrolling.', 'outcome_metric': {'metric': 'checkout_completion_rate', 'baseline': '62%', 'target': '78%'}, 'evidence_link': '../research/x.md', 'audience_renders': {'exec': 'exec text long enough', 'sales': 'sales text long enough', 'support': 'support text long enough', 'customer': 'customer text long enough'}}
BAD = {'narrative_id': 'n1', 'problem': 'stuff', 'who': 'x', 'behaviour_change': 'we added button', 'outcome_metric': {'metric': 'DAU'}, 'evidence_link': '', 'audience_renders': {}}


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
