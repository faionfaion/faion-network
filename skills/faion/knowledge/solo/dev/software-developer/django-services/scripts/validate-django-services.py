#!/usr/bin/env python3
"""validate-django-services.py

Validate the artefact for the django-services methodology against the JSON Schema
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

REQUIRED = ["module_path", "aggregate", "public_functions", "http_imports", "orm_outside_services"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    import re
    if 'module_path' in obj and not re.match(r'^[a-z_]+/services/[a-z_]+\.py$', str(obj['module_path'])):
        errs.append('module_path must match app/services/<aggregate>.py')
    if 'aggregate' in obj and (not isinstance(obj['aggregate'], str) or len(obj['aggregate']) < 2):
        errs.append('aggregate must be >= 2 chars')
    if 'public_functions' in obj and (not isinstance(obj['public_functions'], list) or len(obj['public_functions']) < 1):
        errs.append('public_functions must be non-empty list')
    if 'http_imports' in obj and obj['http_imports'] != 0:
        errs.append('http_imports must be 0')
    if 'orm_outside_services' in obj and obj['orm_outside_services'] != 0:
        errs.append('orm_outside_services must be 0')
    return errs


OK = {'module_path': 'app/services/orders.py', 'aggregate': 'orders', 'public_functions': ['place_order', 'cancel_order'], 'http_imports': 0, 'orm_outside_services': 0, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'module_path': 'app/views/orders.py', 'aggregate': 'o', 'public_functions': [], 'http_imports': 3, 'orm_outside_services': 5}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
