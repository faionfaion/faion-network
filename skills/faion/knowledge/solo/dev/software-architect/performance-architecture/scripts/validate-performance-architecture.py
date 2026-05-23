#!/usr/bin/env python3
"""validate-performance-architecture.py

Validate the artefact produced by the performance-architecture methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('spec_id', 'slo', 'baseline', 'cache_topology', 'load_test_gate', 'scaling_triggers', 'version', 'last_reviewed',)
ENUMS: dict[str, list] = {}


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


OK = {'spec_id': 'perf-storefront-2026-05', 'slo': {'p50_ms': 80, 'p95_ms': 200, 'p99_ms': 500, 'availability_pct': 99.9}, 'baseline': {'p95_ms_observed': 320, 'rps_observed': 300}, 'cache_topology': [{'layer': 'cdn', 'scope': 'GET /items list', 'ttl_s': 60}, {'layer': 'redis', 'scope': 'hot SKU detail', 'ttl_s': 600}], 'load_test_gate': {'tool': 'k6', 'thresholds': {'http_req_duration': ['p(95)<200', 'p(99)<500'], 'http_req_failed': ['rate<0.001']}}, 'scaling_triggers': [{'signal': 'cpu_pct', 'threshold': '>70 for 5m'}, {'signal': 'p95_ms', 'threshold': '>180 for 5m'}], 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'spec_id': 'perf 1', 'slo': {'p50_ms': 0, 'p95_ms': 0, 'p99_ms': 0, 'availability_pct': 50}, 'baseline': {'p95_ms_observed': 0, 'rps_observed': 0}, 'cache_topology': [], 'load_test_gate': {'tool': 'manual', 'thresholds': {}}, 'version': '1.0', 'last_reviewed': 'today'}


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
        prog="validate-performance-architecture.py",
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
