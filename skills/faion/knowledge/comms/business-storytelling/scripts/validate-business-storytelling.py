#!/usr/bin/env python3
"""validate-business-storytelling.py

Validate the artefact for the business-storytelling methodology against the schema in
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

REQUIRED = ['artefact_type', 'framework', 'audience', 'central_claim', 'body']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    framework = obj.get("framework")
    if framework not in ["pyramid", "scqa", "pixar"]:
        errs.append(f"framework must be one of pyramid/scqa/pixar, got: {framework!r}")
    cc = obj.get("central_claim") or ""
    if len(cc) > 200:
        errs.append(f"central_claim too long ({len(cc)} > 200)")

    return errs


OK = {   'artefact_type': 'exec-summary',
    'framework': 'pyramid',
    'audience': 'Series-A board, 5-min read',
    'central_claim': 'We should retire product line B in Q3 and redirect engineering to line A '
                     'growth.',
    'body': {   'lead': 'Retire product line B in Q3.',
                'support_1': 'Line B revenue is 8% of total and declining 15% QoQ.',
                'support_2': "Engineering hours on B (40%) cap A's growth velocity at half "
                             'capacity.',
                'support_3': 'Customer overlap is 70% — line B churn risk to A is contained.',
                'so_what_1': '8% declining means line B is not the future cash engine.',
                'so_what_2': "Reclaiming 40% of engineering doubles A's velocity for the "
                             'high-growth quarter.',
                'so_what_3': 'Low standalone B-only retention means retirement risk is bounded.'}}
BAD = {'artefact_type': 'memo', 'central_claim': 'stuff'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"ok rejected: {errs_ok}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
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
