#!/usr/bin/env python3
"""validate-paid-trial-task-library.py — F-066 B4 stdlib validator for the Paid Trial Task Library artefact.

Validates that an input JSON file satisfies the required-keys subset of the
schema declared in content/02-output-contract.xml of this methodology.

Inputs:
    --file PATH       path to artefact JSON file
    --self-test       run built-in pass/fail fixtures
    --help            show this message

Exit codes:
    0 — valid
    1 — invalid (violations printed to stderr)
    2 — usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['library_id', 'tasks']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
        elif obj[k] is None:
            errs.append(f"required field is null: {k}")
    return errs


OK_FIXTURE = json.loads('{"library_id": "ptl-2026-eng", "tasks": [{"task_id": "be-001", "discipline": "backend", "time_box_hours": 4, "payout": {"amount": 200, "currency": "EUR"}, "deliverable": "PR to scoped sandbox repo implementing /v1/echo with input validation + unit tests", "rubric": [{"criterion": "Tests pass", "good": "all tests + edge cases", "fail": "tests missing or skipped"}, {"criterion": "Input validation", "good": "rejects malformed inputs with clear errors", "fail": "accepts arbitrary input"}, {"criterion": "Code readability", "good": "single-purpose functions <30 LOC", "fail": "200-LOC handler"}], "ip_safe": true}]}')
BAD_FIXTURE = json.loads('{"tasks": [{"task_id": "be-001", "time_box_hours": 4, "payout": {"amount": 0, "currency": "EUR"}, "deliverable": "do a discovery call and write notes", "rubric": []}]}')


def self_test() -> int:
    errs = validate(OK_FIXTURE)
    if errs:
        sys.stderr.write("self-test: valid fixture rejected — " + "; ".join(errs) + "\n")
        return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("self-test: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
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
        sys.stderr.write(f"json parse error: {e}\n")
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
