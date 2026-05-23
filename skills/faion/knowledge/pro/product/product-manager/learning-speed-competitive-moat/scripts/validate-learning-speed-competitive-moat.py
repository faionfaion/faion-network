#!/usr/bin/env python3
"""validate-learning-speed-competitive-moat.py

Validate the artefact produced by the learning-speed-competitive-moat methodology against the JSON
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

REQUIRED = ['audit_period', 'beliefs', 'decision_velocity', 'loss_attribution']
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
    if not _re.match(r'^[0-9]{4}-Q[1-4]$', obj.get('audit_period') or ''):
        errs.append('audit_period must match YYYY-QX')
    for b in obj.get('beliefs') or []:
        c = b.get('confidence')
        if not isinstance(c, (int, float)) or not (0 <= c <= 1):
            errs.append(f'belief {b.get("id")!r} confidence out of [0,1]')
        if b.get('evidence_type') not in ('interview', 'experiment', 'metric', 'literature', 'intuition'):
            errs.append(f'belief {b.get("id")!r} evidence_type invalid')
    dv = obj.get('decision_velocity') or {}
    for k in ('p0_avg_days', 'p1_avg_days', 'p2_avg_days', 'decisions_this_quarter'):
        v = dv.get(k)
        if v is None or v < 0:
            errs.append(f'decision_velocity.{k} must be non-negative')
    la = obj.get('loss_attribution') or {}
    if (la.get('losses_total') or 0) > 0 and not la.get('by_cause'):
        errs.append('loss_attribution.losses_total > 0 with empty by_cause')
    return errs


GOOD = {'audit_period': '2026-Q2', 'beliefs': [{'id': 'b1', 'statement': 'MSPs will pay for usage-based.', 'confidence': 0.55, 'last_update': '2026-04-12', 'evidence_type': 'interview', 'stale_flag': False}], 'decision_velocity': {'p0_avg_days': 8.2, 'p1_avg_days': 2.1, 'p2_avg_days': 0.3, 'decisions_this_quarter': 47}, 'loss_attribution': {'losses_total': 6, 'by_cause': {'shipped-sooner': 3}}, 'kill_criteria_present': True}
BAD = {'audit_period': '2026', 'beliefs': [{'id': 'b1', 'statement': 'vibes', 'confidence': 1.5, 'last_update': 'soon', 'evidence_type': 'guess'}], 'decision_velocity': {'p0_avg_days': -1, 'p1_avg_days': 0, 'p2_avg_days': 0, 'decisions_this_quarter': -5}, 'loss_attribution': {'losses_total': 6, 'by_cause': {}}}


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
