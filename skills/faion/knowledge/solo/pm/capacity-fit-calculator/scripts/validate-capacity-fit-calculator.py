#!/usr/bin/env python3
"""validate-capacity-fit-calculator.py — validate a capacity-fit-calculator output JSON against the methodology schema.

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

REQUIRED = ['artefact_id', 'version', 'last_reviewed', 'sprint_id', 'baseline_velocity', 'focus_factor', 'reductions', 'available_capacity', 'proposed_scope', 'fit_decision', 'owner']
ENUMS = {'fit_decision': ['fits', 'cut-required', 'expand-allowed']}
SEMVER_FIELDS = ['version']
DATE_FIELDS = ['last_reviewed']
INT_FIELDS = []
NUM_FIELDS = ['baseline_velocity', 'focus_factor', 'available_capacity', 'proposed_scope']
ARRAY_FIELDS = ['reductions']
OBJECT_FIELDS = []
BOOL_FIELDS = []
STRING_FIELDS = ['artefact_id', 'sprint_id', 'fit_decision', 'owner']
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


VALID_FIXTURE = json.loads('{"artefact_id": "capacity-fit-2026-w22", "version": "1.0.0", "last_reviewed": "2026-05-23", "sprint_id": "2026-W22", "baseline_velocity": 24, "focus_factor": 0.75, "reductions": [{"reason": "ruslan-pto-1d", "points": 4}], "available_capacity": 14, "proposed_scope": 16, "fit_decision": "cut-required", "owner": "@ruslan"}')
INVALID_FIXTURE = json.loads('{"sprint_id": "2026-W22", "baseline_velocity": 24, "focus_factor": 0.95, "reductions": [], "available_capacity": 22, "proposed_scope": 30, "fit_decision": "fits", "owner": "team"}')


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
