#!/usr/bin/env python3
"""validate-feedback-management.py

Validate the artefact produced by the feedback-management methodology against the JSON
Schema in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    path to artefact JSON
    --self-test    run built-in fixtures
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['item_id', 'source', 'date', 'user_id', 'verbatim', 'classification']
ENUMS = {'source': ['support', 'nps', 'app-store', 'in-app', 'sales', 'social'], 'disposition': ['will-do', 'under-consideration', 'wont-do', 'pending']}


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    for field, allowed in ENUMS.items():
        v = obj.get(field)
        if v is not None and v not in allowed:
            errs.append(f"{field} must be one of {sorted(allowed)} (got {v!r})")
    import re as _re
    if len((obj.get('verbatim') or '')) < 10:
        errs.append('verbatim too short (need >= 10 chars)')
    if not obj.get('user_id'):
        errs.append('user_id must be non-empty')
    cls = obj.get('classification') or {}
    tp = cls.get('taxonomy_path') or ''
    if not _re.match(r'^[a-z][a-z0-9-]+(/[a-z][a-z0-9-]+){0,2}$', tp):
        errs.append(f'classification.taxonomy_path invalid: {tp!r}')
    return errs


GOOD = {'item_id': 'fb-1', 'source': 'support', 'date': '2026-05-19', 'user_id': 'U_3471', 'verbatim': 'export crashes above 1000 rows', 'classification': {'taxonomy_path': 'performance/export/large-dataset'}}
BAD = {'item_id': 'fb1', 'source': 'wechat', 'date': 'May 19', 'user_id': '', 'verbatim': 'bug', 'classification': {'taxonomy_path': 'Performance/Bug'}}


def self_test():
    errs_good = validate(GOOD)
    if errs_good:
        sys.stderr.write(f"GOOD rejected: {errs_good}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to artefact JSON")
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
