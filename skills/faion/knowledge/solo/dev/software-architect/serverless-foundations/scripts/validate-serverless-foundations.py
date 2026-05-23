#!/usr/bin/env python3
"""validate-serverless-foundations.py

Validate the artefact produced by the serverless-foundations methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run built-in OK + BAD fixtures
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED: tuple[str, ...] = ('checklist_id', 'items', 'verdict', 'version', 'last_reviewed',)
ENUMS: dict[str, list] = {'verdict': ['proceed', 'request-changes', 'abort']}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k, allowed in ENUMS.items():
        if k in obj and obj[k] not in allowed:
            errs.append(f"field {k!r} not in allowed values {allowed!r}; got {obj[k]!r}")
    return errs


OK = {'checklist_id': 'slsf-webhook-2026-05', 'items': [{'id': 1, 'verdict': 'yes', 'rationale': 'Webhook handler runs <500ms; fits Lambda limits.'}, {'id': 2, 'verdict': 'yes', 'rationale': 'Stateless; state in DynamoDB.'}, {'id': 3, 'verdict': 'yes', 'rationale': 'SQS-only trigger.'}, {'id': 4, 'verdict': 'yes', 'rationale': 'Cold start 200ms acceptable; no PC needed.'}, {'id': 5, 'verdict': 'yes', 'rationale': 'Dedup by event_id.'}, {'id': 6, 'verdict': 'yes', 'rationale': 'X-Ray + correlation id middleware.'}, {'id': 7, 'verdict': 'yes', 'rationale': 'Secrets Manager + 90d rotation.'}, {'id': 8, 'verdict': 'yes', 'rationale': 'SAM template covers all resources.'}, {'id': 9, 'verdict': 'yes', 'rationale': 'Lock-in noted: SQS + Lambda; exit cost ~2 sprint-weeks.'}, {'id': 10, 'verdict': 'yes', 'rationale': 'Break-even RPS = 250; current 20 RPS.'}], 'verdict': 'proceed', 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'checklist_id': 'slsf 1', 'items': [{'id': 1, 'verdict': 'maybe', 'rationale': ''}], 'verdict': 'yes', 'version': '1.0', 'last_reviewed': 'today'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-serverless-foundations.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
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
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
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
