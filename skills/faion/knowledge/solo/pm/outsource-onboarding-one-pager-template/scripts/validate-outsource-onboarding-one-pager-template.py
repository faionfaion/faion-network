#!/usr/bin/env python3
"""validate-outsource-onboarding-one-pager-template.py — validate a outsource-onboarding-one-pager-template output JSON against the methodology schema.

Inputs:
    --file PATH    JSON file to validate
    --self-test    run built-in valid + invalid fixtures
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ['artefact_id', 'version', 'last_reviewed', 'contractor', 'scope', 'deliverables', 'comms_cadence', 'access_list', 'payment_terms', 'kill_switch', 'owner']
ENUMS = {}
SEMVER_FIELDS = ['version']
DATE_FIELDS = ['last_reviewed']
INT_FIELDS = []
NUM_FIELDS = []
ARRAY_FIELDS = ['deliverables', 'access_list']
OBJECT_FIELDS = ['contractor', 'comms_cadence', 'payment_terms', 'kill_switch']
BOOL_FIELDS = []
STRING_FIELDS = ['artefact_id', 'scope', 'owner']
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _type_ok(val, expected: str) -> bool:
    if expected == "string":
        return isinstance(val, str)
    if expected == "integer":
        return isinstance(val, int) and not isinstance(val, bool)
    if expected == "number":
        return isinstance(val, (int, float)) and not isinstance(val, bool)
    if expected == "array":
        return isinstance(val, list)
    if expected == "object":
        return isinstance(val, dict)
    if expected == "boolean":
        return isinstance(val, bool)
    return True


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k, allowed in ENUMS.items():
        if k in obj and obj[k] not in allowed:
            errs.append(f"{k} not in enum {allowed!r}: got {obj[k]!r}")
    for k in SEMVER_FIELDS:
        if k in obj and not SEMVER_RE.match(str(obj[k])):
            errs.append(f"{k} must be semver MAJOR.MINOR.PATCH; got {obj[k]!r}")
    for k in DATE_FIELDS:
        if k in obj and not DATE_RE.match(str(obj[k])):
            errs.append(f"{k} must be YYYY-MM-DD; got {obj[k]!r}")
    for k in INT_FIELDS:
        if k in obj and not _type_ok(obj[k], "integer"):
            errs.append(f"{k} must be integer; got {type(obj[k]).__name__}")
    for k in NUM_FIELDS:
        if k in obj and not _type_ok(obj[k], "number"):
            errs.append(f"{k} must be number; got {type(obj[k]).__name__}")
    for k in ARRAY_FIELDS:
        if k in obj and not _type_ok(obj[k], "array"):
            errs.append(f"{k} must be array; got {type(obj[k]).__name__}")
    for k in OBJECT_FIELDS:
        if k in obj and not _type_ok(obj[k], "object"):
            errs.append(f"{k} must be object; got {type(obj[k]).__name__}")
    for k in BOOL_FIELDS:
        if k in obj and not _type_ok(obj[k], "boolean"):
            errs.append(f"{k} must be boolean; got {type(obj[k]).__name__}")
    for k in STRING_FIELDS:
        if k in obj and not _type_ok(obj[k], "string"):
            errs.append(f"{k} must be string; got {type(obj[k]).__name__}")
    return errs


VALID_FIXTURE = json.loads('{"artefact_id": "onboard-contractor-x-2026-w22", "version": "1.0.0", "last_reviewed": "2026-05-23", "contractor": {"name": "designer-x", "agreement_signed": "2026-05-22"}, "scope": "Lead designer for /pricing redesign + /home hero refresh; output Figma files + production-ready assets.", "deliverables": [{"id": "d1", "what": "/pricing v1 wireframe", "due_in_hours": 24}, {"id": "d2", "what": "/pricing final mocks", "due_in_hours": 168}], "comms_cadence": {"daily_standup": "#daily-standup by 11:00", "weekly_call": "Friday 14:00 30min"}, "access_list": [{"tool": "figma", "level": "edit"}, {"tool": "slack", "level": "guest"}, {"tool": "github", "level": "read"}], "payment_terms": {"rate": 80, "currency": "EUR", "cycle": "biweekly", "via": "wise"}, "kill_switch": {"trial_period_weeks": 2, "criterion": "first 2 deliverables on time AND figma fidelity", "exit_pay_days": 14}, "owner": "@ruslan"}')
INVALID_FIXTURE = json.loads('{"contractor": {"name": "x"}, "scope": "general help with stuff", "deliverables": [], "comms_cadence": {}, "access_list": [], "payment_terms": {}, "kill_switch": {}, "owner": "team"}')


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write("valid fixture rejected:\n")
        for e in errs:
            sys.stderr.write(f"  {e}\n")
        return 1
    if not validate(INVALID_FIXTURE):
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
