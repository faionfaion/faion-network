#!/usr/bin/env python3
"""validate-mcp.py

Validate the spec artefact for the mcp methodology against the schema in
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

REQUIRED = ['server_name', 'transport', 'tools', 'credentials', 'smoke_test_result']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'server_name': 'internal-bigquery', 'transport': 'stdio', 'tools': [{'name': 'query_dataset', 'description': 'Run a SELECT-only query against allowed datasets.', 'schema_uri': 'schemas/query.json'}], 'credentials': {'env_vars': ['GOOGLE_APPLICATION_CREDENTIALS'], 'min_scope': True}, 'smoke_test_result': {'passed': True, 'timestamp': '2026-05-22T10:00:00Z'}, 'package_uri': 'npm:@acme/internal-bigquery-mcp'}
BAD = {'server_name': 'x'}


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
