#!/usr/bin/env python3
"""validate-django-services.py

Validate the artefact produced by the django-services methodology against the JSON
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
import re
import sys
from pathlib import Path

REQUIRED: tuple[str, ...] = ('service_name', 'module_path', 'aggregate', 'kw_only', 'type_hints_complete', 'write_count', 'atomic', 'side_effects_on_commit', 'http_imports', 'orm_outside_services', 'tests_path')
ENUMS: dict[str, list] = {}
MODULE_PATH_RE = re.compile(r'^[a-z_][a-z0-9_]*(\.[a-z_][a-z0-9_]*)*\.services(\.[a-z_][a-z0-9_]*)?$')
MUST_BE_ZERO: tuple[str, ...] = ('http_imports', 'orm_outside_services')


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
    if 'module_path' in obj and not MODULE_PATH_RE.match(str(obj['module_path'])):
        errs.append("field 'module_path' must be a dotted path ending in .services[.<aggregate>]")
    if 'aggregate' in obj and (not isinstance(obj['aggregate'], str) or len(obj['aggregate']) < 2):
        errs.append("field 'aggregate' must be a string of >=2 chars")
    if 'public_functions' in obj and (not isinstance(obj['public_functions'], list) or len(obj['public_functions']) < 1):
        errs.append("field 'public_functions' must be a non-empty list")
    for k in MUST_BE_ZERO:
        if k in obj and obj[k] != 0:
            errs.append(f"field {k!r} must be 0; got {obj[k]!r}")
    return errs


OK = {'service_name': 'order_create', 'module_path': 'apps.orders.services', 'aggregate': 'orders', 'public_functions': ['order_create', 'order_cancel'], 'kw_only': True, 'type_hints_complete': True, 'write_count': 3, 'atomic': True, 'side_effects_on_commit': ['apps.orders.tasks.send_order_confirmation.delay'], 'http_imports': 0, 'orm_outside_services': 0, 'validated_at': '2026-05-23T10:00:00Z', 'tests_path': 'apps/orders/tests/test_services.py'}
BAD = {'service_name': 'create_order', 'module_path': 'apps.orders.views', 'aggregate': 'o', 'public_functions': [], 'atomic': False, 'write_count': 4, 'http_imports': 3, 'orm_outside_services': 5}


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
        prog="validate-django-services.py",
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
