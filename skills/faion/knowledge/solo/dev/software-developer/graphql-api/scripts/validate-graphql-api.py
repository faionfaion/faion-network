#!/usr/bin/env python3
"""validate-graphql-api.py

Validate the artefact for the graphql-api methodology against the JSON Schema
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

REQUIRED = ["schema_path", "types_count", "queries_count", "mutations_count", "dataloader_count", "depth_limit", "complexity_limit", "diff_gate_enabled"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'schema_path' in obj and (not isinstance(obj['schema_path'], str) or len(obj['schema_path']) < 3):
        errs.append('schema_path must be >= 3 chars')
    if 'types_count' in obj and (not isinstance(obj['types_count'], int) or obj['types_count'] < 1):
        errs.append('types_count must be int >= 1')
    if 'queries_count' in obj and (not isinstance(obj['queries_count'], int) or obj['queries_count'] < 1):
        errs.append('queries_count must be int >= 1')
    if 'depth_limit' in obj and (not isinstance(obj['depth_limit'], int) or obj['depth_limit'] < 3 or obj['depth_limit'] > 12):
        errs.append('depth_limit must be int in [3,12]')
    if 'complexity_limit' in obj and (not isinstance(obj['complexity_limit'], int) or obj['complexity_limit'] < 100):
        errs.append('complexity_limit must be int >= 100')
    return errs


OK = {'schema_path': 'src/schema.graphql', 'types_count': 24, 'queries_count': 12, 'mutations_count': 6, 'dataloader_count': 7, 'depth_limit': 7, 'complexity_limit': 1000, 'diff_gate_enabled': True, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'schema_path': 'x', 'types_count': 0, 'queries_count': 0, 'depth_limit': 1}


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
