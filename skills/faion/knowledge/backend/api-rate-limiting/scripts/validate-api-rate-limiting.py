#!/usr/bin/env python3
"""validate-api-rate-limiting.py

Validate a API Rate Limiting artefact against the JSON Schema (draft-07) declared in
`content/02-output-contract.xml`. Stdlib-only; no external pip deps.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable / parse error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = [
    "artefact_id",
    "api_id",
    "algorithm",
    "tiers",
    "per_endpoint_multipliers",
    "backend",
    "headers",
    "over_limit_response",
    "evidence",
    "status",
    "owner",
    "last_touched",
    "template_version"
]

FORBIDDEN_OWNERS = {"team", "us", "tbd", "n/a", "everyone", "all", "design", "engineering", "design-team", "design team", ""}
ALLOWED_STATUS = {"draft", "ready_for_review", "approved", "archived"}

ISO_DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

INT_FIELDS = []
NUM_FIELDS = []
BOOL_FIELDS = []
ARRAY_FIELDS = ["tiers", "headers", "evidence"]
OBJECT_FIELDS = ["per_endpoint_multipliers", "over_limit_response"]
STRING_FIELDS = ["api_id", "algorithm", "backend", "status"]


def _type_ok(val, expected: str) -> bool:
    if expected == "string":
        return isinstance(val, str)
    if expected == "integer":
        return isinstance(val, int) and not isinstance(val, bool)
    if expected == "number":
        return isinstance(val, (int, float)) and not isinstance(val, bool)
    if expected == "boolean":
        return isinstance(val, bool)
    if expected == "array":
        return isinstance(val, list)
    if expected == "object":
        return isinstance(val, dict)
    return True


def validate(obj) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be an object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.strip().lower() in FORBIDDEN_OWNERS:
        errs.append("owner is a generic group: " + repr(owner))
    lt = obj.get("last_touched")
    if isinstance(lt, str) and not ISO_DATETIME.match(lt):
        errs.append("last_touched is not ISO-8601 datetime")
    tv = obj.get("template_version")
    if isinstance(tv, str) and not SEMVER.match(tv):
        errs.append("template_version is not semver")
    status = obj.get("status")
    if isinstance(status, str) and status not in ALLOWED_STATUS:
        errs.append("status not in allowed enum: " + repr(status))
    evidence = obj.get("evidence")
    if isinstance(evidence, list) and len(evidence) == 0:
        errs.append("evidence array is empty")
    for k in INT_FIELDS:
        if k in obj and not _type_ok(obj[k], "integer"):
            errs.append(k + " must be integer; got " + type(obj[k]).__name__)
    for k in NUM_FIELDS:
        if k in obj and not _type_ok(obj[k], "number"):
            errs.append(k + " must be number; got " + type(obj[k]).__name__)
    for k in BOOL_FIELDS:
        if k in obj and not _type_ok(obj[k], "boolean"):
            errs.append(k + " must be boolean; got " + type(obj[k]).__name__)
    for k in ARRAY_FIELDS:
        if k in obj and not _type_ok(obj[k], "array"):
            errs.append(k + " must be array; got " + type(obj[k]).__name__)
    for k in OBJECT_FIELDS:
        if k in obj and not _type_ok(obj[k], "object"):
            errs.append(k + " must be object; got " + type(obj[k]).__name__)
    for k in STRING_FIELDS:
        if k in obj and not _type_ok(obj[k], "string"):
            errs.append(k + " must be string; got " + type(obj[k]).__name__)
    return errs


OK = {'artefact_id': 'api-rate-limiting-2026-05-23', 'owner': 'ruslan@faion.net', 'last_touched': '2026-05-23T12:00:00Z', 'template_version': '1.1.0', 'status': 'ready_for_review', 'evidence': [{'source': 'https://example.com/source-1', 'citation': 'verbatim quote from source'}], 'api_id': 'draft', 'algorithm': 'draft', 'tiers': ['draft-item'], 'per_endpoint_multipliers': {'key': 'value'}, 'backend': 'draft', 'headers': ['draft-item'], 'over_limit_response': {'key': 'value'}}
BAD = {"foo": "bar"}


def self_test() -> int:
    errs = validate(OK)
    if errs:
        sys.stderr.write("self-test FAIL: valid fixture rejected: " + repr(errs) + "\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
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
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write("JSON parse error: " + str(e) + "\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
