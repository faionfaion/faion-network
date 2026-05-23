#!/usr/bin/env python3
"""validate-go-standard-layout.py

Validate the artefact for the go-standard-layout methodology against the JSON Schema
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

REQUIRED = ["feature_path", "handler_logic_lines", "service_present", "repo_present", "http_imports_in_service", "db_imports_in_handler"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    import re
    if 'feature_path' in obj and not re.match(r'^internal/[a-z_]+$', str(obj['feature_path'])):
        errs.append('feature_path must match internal/<feature>')
    if 'handler_logic_lines' in obj and (not isinstance(obj['handler_logic_lines'], int) or obj['handler_logic_lines'] > 50):
        errs.append('handler_logic_lines must be int <= 50')
    if 'http_imports_in_service' in obj and obj['http_imports_in_service'] != 0:
        errs.append('http_imports_in_service must be 0')
    if 'db_imports_in_handler' in obj and obj['db_imports_in_handler'] != 0:
        errs.append('db_imports_in_handler must be 0')
    return errs


OK = {'feature_path': 'internal/orders', 'handler_logic_lines': 12, 'service_present': True, 'repo_present': True, 'http_imports_in_service': 0, 'db_imports_in_handler': 0, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'feature_path': 'app/orders', 'handler_logic_lines': 180, 'service_present': False, 'http_imports_in_service': 2}


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
