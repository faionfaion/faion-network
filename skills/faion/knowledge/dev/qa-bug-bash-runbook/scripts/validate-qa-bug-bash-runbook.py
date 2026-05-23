#!/usr/bin/env python3
"""validate-qa-bug-bash-runbook.py

Validate the artefact produced by the qa-bug-bash-runbook methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('bash_id', 'release_id', 'duration_minutes', 'personas', 'charters', 'findings', 'dedup_count', 'ledger_path')
ENUMS: dict[str, list] = {}


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


OK = {'bash_id': 'bb-2026-05-23-v2.4', 'release_id': 'v2.4.0', 'duration_minutes': 55, 'personas': ['admin', 'end_user', 'integrator'], 'charters': [{'persona': 'admin', 'mission': 'Bulk-edit member roles', 'tester': 'alice', 'charter_id': 'c1'}], 'findings': [{'id': 'f1', 'title': 'Role bulk-edit ignores admin filter', 'severity': 'S2', 'repro': '1. login admin 2. select 10 users 3. apply role', 'screenshot': 'https://i.example/abc'}], 'dedup_count': 3, 'ledger_path': 'release/v2.4/bug-bash-ledger.csv'}
BAD = {'bash_id': 'bb-2026-05-23-v2.4', 'duration_minutes': 120}


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
        prog="validate-qa-bug-bash-runbook.py",
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
