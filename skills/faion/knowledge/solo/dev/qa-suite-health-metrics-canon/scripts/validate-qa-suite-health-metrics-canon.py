#!/usr/bin/env python3
"""validate-qa-suite-health-metrics-canon.py

Validate the artefact produced by the qa-suite-health-metrics-canon methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('canon_id', 'metrics', 'cadence_days', 'report_window_days', 'latest_report_path')
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


OK = {'canon_id': 'suite-health-1.0', 'metrics': [{'id': 'flake_rate', 'threshold': 0.01, 'direction': 'lower_is_better', 'owner': 'alice', 'route_to_methodology': 'qa-flake-ledger-template'}, {'id': 'p95_runtime_sec', 'threshold': 600, 'direction': 'lower_is_better', 'owner': 'bob', 'route_to_methodology': 'perf-test-tools'}, {'id': 'failure_attribution_pct', 'threshold': 0.9, 'direction': 'higher_is_better', 'owner': 'carol', 'route_to_methodology': 'qa-flaky-test-root-cause-taxonomy'}, {'id': 'coverage_pct', 'threshold': 0.8, 'direction': 'higher_is_better', 'owner': 'dave', 'route_to_methodology': 'qa-test-strategy-template'}, {'id': 'quarantine_count', 'threshold': 10, 'direction': 'lower_is_better', 'owner': 'alice', 'route_to_methodology': 'qa-flake-ledger-template'}, {'id': 'mttd_minutes', 'threshold': 30, 'direction': 'lower_is_better', 'owner': 'eve', 'route_to_methodology': 'qa-rollback-trigger-canon'}], 'cadence_days': 7, 'report_window_days': 14, 'latest_report_path': 'qa/reports/2026-W21.json'}
BAD = {'canon_id': 'suite-health-1.0', 'metrics': []}


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
        prog="validate-qa-suite-health-metrics-canon.py",
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
