#!/usr/bin/env python3
"""validate-graph-rag-production.py

Validate the artefact produced by the graph-rag-production methodology against the
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

REQUIRED = ['service_name', 'router_model', 'cache_backend', 'max_cost_usd_per_query', 'delta_stream', 'slo_p95_seconds', 'alert_webhook']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'service_name': 'graphrag-portfolio', 'router_model': 'claude-haiku-4.5', 'cache_backend': 'valkey', 'max_cost_usd_per_query': {'global': 0.5, 'local': 0.05, 'community': 0.1}, 'delta_stream': 'kafka://graphrag-delta', 'slo_p95_seconds': 5.0, 'alert_webhook': 'https://alerts.example.com/graphrag'}
BAD = {'service_name': 'x', 'cache_backend': 'sqlite'}


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
