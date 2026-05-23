#!/usr/bin/env python3
"""validate-work-breakdown-structure.py

Validate the artefact produced for the work-breakdown-structure methodology against the schema
in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['project', 'baseline_ref', 'nodes']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"project": "checkout-redesign", "baseline_ref": "scope-statement-v2", "nodes": [{"id": "1", "name": "Payment redesign", "level": 1, "is_leaf": false}, {"id": "1.1", "name": "Stripe Payment Intents v2 integration", "level": 2, "is_leaf": false}, {"id": "1.1.1", "name": "API client refactor", "level": 3, "is_leaf": true, "owner": "Iryna", "estimate_hours_low": 16, "estimate_hours_high": 40, "acceptance": "all old SDK calls replaced; integration tests green"}]}')
BAD = json.loads('{"project": "x", "nodes": [{"id": "1", "name": "y", "level": 1, "is_leaf": true}]}')


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: OK fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
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
