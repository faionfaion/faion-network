#!/usr/bin/env python3
"""validate-decision-tree-process.py

Validate the artefact produced by the decision-tree-process methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('report_id', 'question', 'reversibility', 'options', 'matrix_total_weight', 'recommended', 'adr_ref', 'review_trigger', 'review_date', 'version', 'last_reviewed',)
ENUMS: dict[str, list] = {'reversibility': ['one_way', 'two_way']}


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


OK = {'report_id': 'dec-tenant-store-2026-05', 'question': 'Do we adopt Postgres or Mongo for tenant data?', 'reversibility': 'one_way', 'options': ['postgres', 'mongo', 'postgres_jsonb', 'do_nothing_sqlite', 'cockroachdb'], 'matrix_total_weight': 100, 'recommended': 'postgres_jsonb', 'poc_ref': 'poc/postgres-jsonb-7day', 'adr_ref': 'adr-data-014', 'review_trigger': 'Tenant table exceeds 5M rows OR p95 read latency > 80ms.', 'review_date': '2027-05-23', 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'report_id': 'dec 1', 'question': 'what?', 'reversibility': 'maybe', 'options': ['postgres'], 'matrix_total_weight': 80, 'recommended': 'postgres_jsonb', 'adr_ref': '', 'review_trigger': '', 'review_date': 'soon', 'version': '1.0', 'last_reviewed': 'today'}


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
        prog="validate-decision-tree-process.py",
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
