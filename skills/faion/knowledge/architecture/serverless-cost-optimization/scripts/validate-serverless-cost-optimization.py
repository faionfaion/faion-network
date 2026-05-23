#!/usr/bin/env python3
"""validate-serverless-cost-optimization.py

Validate the artefact produced by the serverless-cost-optimization methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('report_id', 'functions', 'before_monthly_usd', 'after_monthly_usd', 'saving_pct', 'actions', 'break_even_rps', 'review_trigger', 'version', 'last_reviewed',)
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


OK = {'report_id': 'cost-checkout-2026-05', 'functions': [{'name': 'checkout-fn', 'configured_memory_mb': 1024, 'p95_memory_mb': 380, 'p95_duration_ms': 120, 'rps': 80}], 'before_monthly_usd': 2000, 'after_monthly_usd': 850, 'saving_pct': 57.5, 'actions': [{'change': 'Tune memory 1024 → 512MB', 'expected_saving_usd': 720}, {'change': 'Replace static PC=10 with auto-scaling PC min=2', 'expected_saving_usd': 400}, {'change': 'BatchGetItem 25 entries per call', 'expected_saving_usd': 250}], 'break_even_rps': 350, 'review_trigger': 'checkout-fn RPS > 350 sustained for 14 days OR Lambda cost > $1500/mo again.', 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'report_id': 'cost 1', 'functions': [], 'before_monthly_usd': -100, 'after_monthly_usd': 0, 'saving_pct': 150, 'actions': [], 'review_trigger': '', 'version': '1.0', 'last_reviewed': 'today'}


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
        prog="validate-serverless-cost-optimization.py",
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
