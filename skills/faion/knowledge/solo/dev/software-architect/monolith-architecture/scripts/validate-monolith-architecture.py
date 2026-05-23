#!/usr/bin/env python3
"""validate-monolith-architecture.py

Validate the artefact produced by the monolith-architecture methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('spec_id', 'internal_layout', 'single_pipeline', 'transaction_strategy', 'scale_plan', 'extraction_triggers', 'version', 'last_reviewed',)
ENUMS: dict[str, list] = {'internal_layout': ['vertical_slice', 'layered'], 'single_pipeline': [True], 'transaction_strategy': ['acid_default', 'documented_exceptions']}


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


OK = {'spec_id': 'mono-shop-mvp-2026-05', 'internal_layout': 'vertical_slice', 'single_pipeline': True, 'transaction_strategy': 'acid_default', 'scale_plan': {'scale_up_budget': 'Up to 8 vCPU / 16 GB RAM on a single instance.', 'scale_out_trigger': 'Sustained > 70% CPU for 7 days OR p95 latency > 200ms.'}, 'extraction_triggers': ['Checkout traffic > 10x rest of system for 30 days.', 'Independent team owns checkout with conflicting release cadence.'], 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'spec_id': 'mono 1', 'internal_layout': 'horizontal', 'single_pipeline': False, 'transaction_strategy': 'saga_by_default', 'scale_plan': {'scale_up_budget': '', 'scale_out_trigger': ''}, 'extraction_triggers': [], 'version': '1.0', 'last_reviewed': 'today'}


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
        prog="validate-monolith-architecture.py",
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
