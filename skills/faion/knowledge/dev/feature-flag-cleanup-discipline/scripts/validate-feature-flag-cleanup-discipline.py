#!/usr/bin/env python3
"""validate-feature-flag-cleanup-discipline.py

Validate a Feature Flag Cleanup Discipline artefact against the JSON Schema (draft-07) defined in
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
    "flag_name",
    "owner",
    "expiry",
    "cleanup_pr",
    "verified_removed_evidence",
    "metric_snapshot",
    "last_touched",
    "template_version",
    "status"
]

FORBIDDEN_OWNERS = {"team", "us", "tbd", "n/a", "everyone", "all", ""}

ISO_DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

ALLOWED_STATUS = {"draft", "ready_for_review", "approved", "archived"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be an object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.strip().lower() in FORBIDDEN_OWNERS:
        errs.append(f"owner is a generic group: {owner!r}")
    last_touched = obj.get("last_touched")
    if isinstance(last_touched, str) and not ISO_DATETIME.match(last_touched):
        errs.append("last_touched is not ISO-8601 datetime")
    tv = obj.get("template_version")
    if isinstance(tv, str) and not SEMVER.match(tv):
        errs.append("template_version is not semver")
    status = obj.get("status")
    if isinstance(status, str) and status not in ALLOWED_STATUS:
        errs.append(f"status not in allowed enum: {status!r}")
    return errs


OK = {'artefact_id': 'feature-flag-cleanup-discipline-2026-05-23', 'owner': 'ruslan@faion.net', 'last_touched': '2026-05-23T12:00:00Z', 'template_version': '1.1.0', 'status': 'ready_for_review', 'flag_name': 'draft', 'expiry': 'draft', 'cleanup_pr': 'draft', 'verified_removed_evidence': 'draft', 'metric_snapshot': {'key': 'value'}}

BAD = {"foo": "bar"}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"self-test FAIL: valid fixture rejected: {errs_ok!r}\n")
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n")
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
