#!/usr/bin/env python3
"""validate-stakeholder-management.py

Validate the artefact produced by the stakeholder-management methodology against the JSON
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

REQUIRED = ['project_id', 'stakeholders', 'decision_rights', 'escalation_triggers', 'upward_comms_cadence']
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
    for s in obj.get('stakeholders') or []:
        for k in ('power', 'interest', 'attitude'):
            if k not in s:
                errs.append(f'stakeholder {s.get("id")!r} missing {k}')
        if s.get('power') not in ('high', 'low'):
            errs.append(f'stakeholder {s.get("id")!r} power invalid')
        if s.get('interest') not in ('high', 'low'):
            errs.append(f'stakeholder {s.get("id")!r} interest invalid')
        if s.get('attitude') not in ('supporter', 'neutral', 'blocker'):
            errs.append(f'stakeholder {s.get("id")!r} attitude invalid')
        eng = s.get('engagement') or {}
        for k in ('frequency', 'channel', 'content'):
            if not eng.get(k):
                errs.append(f'stakeholder {s.get("id")!r} engagement.{k} missing')
    if not (obj.get('decision_rights') or []):
        errs.append('decision_rights empty')
    if not (obj.get('escalation_triggers') or []):
        errs.append('escalation_triggers empty')
    uc = obj.get('upward_comms_cadence') or {}
    for k in ('weekly_status', 'monthly_review'):
        if not uc.get(k):
            errs.append(f'upward_comms_cadence.{k} missing')
    return errs


GOOD = {'project_id': 'p1', 'stakeholders': [{'id': 's1', 'name': 'x', 'power': 'high', 'interest': 'high', 'attitude': 'supporter', 'engagement': {'frequency': 'weekly', 'channel': 'slack', 'content': 'matrix'}}], 'decision_rights': [{'decision_type': 'go', 'rights': [{'stakeholder_id': 's1', 'role': 'D'}]}], 'escalation_triggers': [{'trigger': 'veto', 'escalate_to': 'head'}], 'upward_comms_cadence': {'weekly_status': 'Fri', 'monthly_review': '1st Tue'}}
BAD = {'project_id': 'p1', 'stakeholders': [{'id': 's1', 'name': 'x', 'power': 'very-high', 'interest': 'yes'}], 'decision_rights': [], 'escalation_triggers': [], 'upward_comms_cadence': {}}


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
