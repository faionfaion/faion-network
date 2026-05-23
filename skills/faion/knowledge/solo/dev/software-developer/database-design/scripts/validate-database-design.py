#!/usr/bin/env python3
"""validate-database-design.py

Validate the artefact for the database-design methodology against the JSON Schema
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

REQUIRED = ["schema_id", "version", "tables_count", "foreign_keys_count", "indexes_count", "migration_plan"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    import re
    if 'version' in obj and not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', str(obj['version'])):
        errs.append('version must be semver')
    if 'tables_count' in obj and (not isinstance(obj['tables_count'], int) or obj['tables_count'] < 1):
        errs.append('tables_count must be int >= 1')
    if 'migration_plan' in obj and obj['migration_plan'] not in ('expand-only', 'expand-then-contract', 'new-schema'):
        errs.append('migration_plan not in enum')
    if 'schema_id' in obj and (not isinstance(obj['schema_id'], str) or len(obj['schema_id']) < 3):
        errs.append('schema_id must be >= 3 chars')
    return errs


OK = {'schema_id': 'orders-v2', 'version': '2.0.0', 'tables_count': 6, 'foreign_keys_count': 8, 'indexes_count': 5, 'migration_plan': 'expand-then-contract', 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'schema_id': 'x', 'version': '2.0', 'tables_count': 0, 'migration_plan': 'adhoc'}


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
