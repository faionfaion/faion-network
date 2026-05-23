#!/usr/bin/env python3
"""validate-okr-cascade-multi-squad.py

Validate the artefact produced by the okr-cascade-multi-squad methodology against the JSON
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

REQUIRED = ['quarter', 'company_okrs', 'squads', 'dependency_edges', 'checkin_cadence']
ENUMS = {'checkin_cadence': ['weekly', 'biweekly']}


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
    if not _re.match(r'^[0-9]{4}-Q[1-4]$', obj.get('quarter') or ''):
        errs.append('quarter must match YYYY-QX')
    if not (obj.get('company_okrs') or []):
        errs.append('company_okrs empty')
    sq = obj.get('squads') or []
    if not (1 <= len(sq) <= 6):
        errs.append(f'squads must be 1-6 (got {len(sq)})')
    for s in sq:
        krs = s.get('krs') or []
        if not (3 <= len(krs) <= 5):
            errs.append(f'squad {s.get("id")!r}: KRs must be 3-5 (got {len(krs)})')
        if not (s.get('trace_to_company') or []):
            errs.append(f'squad {s.get("id")!r}: trace_to_company missing')
    for e in obj.get('dependency_edges') or []:
        for k in ('producer', 'consumer', 'deliverable', 'by_date'):
            if not e.get(k):
                errs.append(f'dependency edge missing {k}')
    return errs


GOOD = {'quarter': '2026-Q2', 'company_okrs': [{'id': 'co-1', 'objective': 'Activation doubles', 'krs': ['co-kr-1']}], 'squads': [{'id': 's-checkout', 'objective': 'Remove top-3 friction', 'krs': [{'id': 'k1', 'metric': 'x', 'baseline': 0.6, 'target': 0.8}, {'id': 'k2', 'metric': 'y', 'baseline': 0.2, 'target': 0.4}, {'id': 'k3', 'metric': 'z', 'baseline': 0.01, 'target': 0.005}], 'trace_to_company': ['co-kr-1']}], 'dependency_edges': [{'producer': 's-identity', 'consumer': 's-checkout', 'deliverable': 'SSO API', 'by_date': '2026-05-15'}], 'checkin_cadence': 'weekly'}
BAD = {'quarter': 'Q2', 'company_okrs': [], 'squads': [{'id': 's1', 'objective': 'ok', 'krs': [{'id': 'k1'}], 'trace_to_company': []}], 'dependency_edges': [{'producer': 'x'}], 'checkin_cadence': 'ad-hoc'}


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
