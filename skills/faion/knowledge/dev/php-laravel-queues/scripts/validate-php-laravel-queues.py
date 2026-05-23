#!/usr/bin/env python3
"""validate-php-laravel-queues.py

Validate the code artefact for the php-laravel-queues methodology against the schema in
02-output-contract.xml.

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

REQUIRED = ['job_class', 'constructor_payload_primitive_only', 'tries', 'timeout_s', 'queue_name', 'failed_method_implemented', 'idempotent']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'job_class': 'SendOrderConfirmationJob', 'constructor_payload_primitive_only': True, 'tries': 5, 'timeout_s': 30, 'backoff_seconds': [10, 30, 60, 120, 240], 'queue_name': 'mail', 'failed_method_implemented': True, 'idempotent': True, 'without_overlapping': False}
BAD = {'constructor_payload_primitive_only': False, 'tries': 1, 'timeout_s': 0, 'queue_name': 'default', 'failed_method_implemented': False, 'idempotent': False}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
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
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
