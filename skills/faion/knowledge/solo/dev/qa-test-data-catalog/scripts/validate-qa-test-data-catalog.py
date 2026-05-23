#!/usr/bin/env python3
"""validate-qa-test-data-catalog.py

Validate the artefact produced by the qa-test-data-catalog methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('catalog_id', 'fixtures', 'blocked_patterns', 'stale_threshold_days', 'last_reviewed')
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


OK = {'catalog_id': 'test-data-v3', 'fixtures': [{'id': 'order-paid-eur', 'owner_service': 'orders', 'refresh': 'function', 'contains_pii': False, 'factory_path': 'apps.orders.tests.factories.PaidOrderEurFactory', 'consumers': ['apps/orders/tests/test_refund.py', 'apps/payments/tests/test_payout.py']}], 'blocked_patterns': ['Order\\.objects\\.create', 'User\\.objects\\.create_user'], 'stale_threshold_days': 60, 'last_reviewed': '2026-05-23'}
BAD = {'catalog_id': 'test-data-v3', 'fixtures': [{'id': 'weird'}]}


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
        prog="validate-qa-test-data-catalog.py",
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
