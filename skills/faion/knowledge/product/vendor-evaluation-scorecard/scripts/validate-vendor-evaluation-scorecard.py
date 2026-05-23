#!/usr/bin/env python3
"""validate-vendor-evaluation-scorecard.py

Validate the artefact produced by the vendor-evaluation-scorecard methodology against the
JSON Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in valid + invalid fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['category', 'vendors', 'weights', 'scores', 'winner', 'exit_cost_eng_days']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'category': 'vector-db', 'vendors': ['qdrant-cloud', 'pinecone', 'weaviate-cloud'], 'weights': {'quality': 0.25, 'cost': 0.2, 'lock_in': 0.2, 'security': 0.2, 'sla': 0.15}, 'scores': {'qdrant-cloud': {'quality': 0.9, 'cost': 0.8, 'lock_in': 0.9, 'security': 0.85, 'sla': 0.8}, 'pinecone': {'quality': 0.92, 'cost': 0.6, 'lock_in': 0.5, 'security': 0.9, 'sla': 0.9}, 'weaviate-cloud': {'quality': 0.85, 'cost': 0.7, 'lock_in': 0.8, 'security': 0.8, 'sla': 0.8}}, 'winner': 'qdrant-cloud', 'exit_cost_eng_days': {'qdrant-cloud': 5, 'pinecone': 25, 'weaviate-cloud': 12}}
BAD = {'category': 'x', 'vendors': ['only-one']}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: valid example rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: invalid example accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    except Exception as exc:
        sys.stderr.write(f"unreadable JSON: {exc}\n")
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
