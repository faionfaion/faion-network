#!/usr/bin/env python3
"""validate-nodejs-service-layer.py

Validate the artefact for the nodejs-service-layer methodology against the JSON Schema
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

REQUIRED = ["feature_path", "controller_present", "service_present", "repo_present", "http_imports_in_service", "orm_imports_in_controller"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'feature_path' in obj and (not isinstance(obj['feature_path'], str) or len(obj['feature_path']) < 3):
        errs.append('feature_path must be >= 3 chars')
    if 'http_imports_in_service' in obj and obj['http_imports_in_service'] != 0:
        errs.append('http_imports_in_service must be 0')
    if 'orm_imports_in_controller' in obj and obj['orm_imports_in_controller'] != 0:
        errs.append('orm_imports_in_controller must be 0')
    for b in ('controller_present', 'service_present', 'repo_present'):
        if b in obj and not isinstance(obj[b], bool):
            errs.append(b + ' must be boolean')
    return errs


OK = {'feature_path': 'src/features/orders', 'controller_present': True, 'service_present': True, 'repo_present': True, 'http_imports_in_service': 0, 'orm_imports_in_controller': 0, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'feature_path': 'x', 'controller_present': True, 'service_present': False, 'http_imports_in_service': 3, 'orm_imports_in_controller': 5}


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
