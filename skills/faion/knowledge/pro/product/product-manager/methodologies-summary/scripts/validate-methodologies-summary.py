#!/usr/bin/env python3
"""validate-methodologies-summary.py

Validate the artefact produced by the methodologies-summary methodology against the JSON
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

REQUIRED = ['task_summary', 'signals', 'selected_methodology', 'rationale']
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
    if not _re.match(r'^[a-z][a-z0-9-]+$', obj.get('selected_methodology') or ''):
        errs.append('selected_methodology must be kebab-case slug')
    sig = obj.get('signals') or {}
    for k in ('artifact', 'horizon', 'decision_shape'):
        if not sig.get(k):
            errs.append(f'signals.{k} missing')
    if len((obj.get('rationale') or '')) < 20:
        errs.append('rationale too short (need >= 20 chars)')
    if obj.get('selected_methodology') == 'methodologies-summary' and not obj.get('fallback_used'):
        errs.append('selected_methodology=methodologies-summary requires fallback_used=true')
    return errs


GOOD = {'task_summary': 'Prioritize 9 quarterly bets across 2 squads.', 'signals': {'artifact': 'okr', 'horizon': 'this-quarter', 'decision_shape': 'cascade'}, 'selected_methodology': 'okr-cascade-multi-squad', 'rationale': 'OKR artifact + quarterly horizon + cascade shape uniquely routes to okr-cascade-multi-squad.', 'fallback_used': False}
BAD = {'task_summary': 'do stuff', 'signals': {'artifact': 'thing'}, 'selected_methodology': 'DoStuff', 'rationale': 'ok'}


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
