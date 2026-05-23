#!/usr/bin/env python3
"""validate-csharp-aspnet-core.py

Validate the artefact for csharp-aspnet-core against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (rc=0 if both pass)
    --help            this message

Exit codes:
    0 = valid (or self-test passed)
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['layering', 'dbcontext_lifetime', 'cancellation_token_propagated', 'error_format', 'dto_kind', 'time_provider', 'test_db_strategy', 'pagination', 'loading', 'transactions']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK_FIXTURE = '{"layering": "controller-service-repository", "dbcontext_lifetime": "scoped", "cancellation_token_propagated": true, "error_format": "problem-details-rfc7807", "dto_kind": "record", "time_provider": true, "test_db_strategy": "testcontainers", "pagination": "keyset", "loading": "eager-include", "transactions": "explicit"}'
BAD_FIXTURE = '{"dbcontext_lifetime": "singleton", "cancellation_token_propagated": false, "error_format": "raw-exception-message", "dto_kind": "ef-entity", "time_provider": false, "test_db_strategy": "ef-in-memory", "pagination": "skip-take", "loading": "lazy", "transactions": "implicit"}'


def self_test() -> int:
    """Built-in fixtures: OK_FIXTURE accepted, BAD_FIXTURE rejected."""
    if validate(json.loads(OK_FIXTURE)):
        sys.stderr.write("self-test FAIL: valid fixture rejected\n")
        return 1
    if not validate(json.loads(BAD_FIXTURE)):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
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
