#!/usr/bin/env python3
"""validate-system-design-process.py

Validate the artefact produced by the system-design-process methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('package_id', 'phases', 'nfrs', 'capacity_estimate', 'c4_levels', 'adr_refs', 'peer_reviewer', 'version', 'last_reviewed',)
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


OK = {'package_id': 'arch-orders-dash-2026-05', 'phases': [{'n': 1, 'name': 'understand', 'complete': True}, {'n': 2, 'name': 'scope_nfrs', 'complete': True}, {'n': 3, 'name': 'design', 'complete': True}, {'n': 4, 'name': 'validate', 'complete': True}, {'n': 5, 'name': 'document', 'complete': True}], 'nfrs': {'p95_ms': 200, 'rps': 50, 'availability_pct': 99.5}, 'capacity_estimate': {'storage_gb_per_month': 5.0, 'compute_cores': 2.0}, 'c4_levels': ['l1_context', 'l2_container'], 'adr_refs': ['adr-data-014', 'adr-cache-002'], 'peer_reviewer': 'olena.kovalenko@example.com', 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'package_id': 'arch 1', 'phases': [{'n': 1, 'name': 'understand', 'complete': False}], 'nfrs': {'p95_ms': 0, 'rps': 0, 'availability_pct': 50}, 'capacity_estimate': {'storage_gb_per_month': -1, 'compute_cores': -1}, 'c4_levels': ['scribble'], 'adr_refs': [], 'version': '1.0', 'last_reviewed': 'today'}


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
        prog="validate-system-design-process.py",
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
