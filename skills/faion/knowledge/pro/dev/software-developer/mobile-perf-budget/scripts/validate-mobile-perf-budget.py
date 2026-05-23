#!/usr/bin/env python3
"""validate-mobile-perf-budget.py

Validate the spec artefact for the mobile-perf-budget methodology against the schema in
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

REQUIRED = ['route', 'lcp_ms', 'inp_ms', 'cls', 'transfer_total_kb', 'js_gz_kb', 'image_kb', 'ci_enforced']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'route': '/', 'lcp_ms': 2200, 'inp_ms': 150, 'cls': 0.05, 'transfer_total_kb': 1200, 'js_gz_kb': 170, 'image_kb': 700, 'tbt_ms': 250, 'ci_enforced': True, 'validation_env': 'lighthouse-mobile'}
BAD = {'lcp_ms': 4500, 'inp_ms': 800, 'cls': 0.4, 'transfer_total_kb': 3500, 'js_gz_kb': 800, 'image_kb': 2500, 'tbt_ms': 1200, 'ci_enforced': False, 'validation_env': 'lighthouse-desktop'}


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
