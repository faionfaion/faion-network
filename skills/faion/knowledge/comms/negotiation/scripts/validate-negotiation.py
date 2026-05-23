#!/usr/bin/env python3
"""validate-negotiation.py

Validate the artefact for the negotiation methodology against the schema in
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

REQUIRED = ['my_batna', 'my_reserve', 'their_reserve_estimate', 'interests', 'objective_criteria', 'cialdini_levers']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    batna = obj.get("my_batna") or {}
    if not isinstance(batna, dict) or not batna.get("name") or not batna.get("value"):
        errs.append("my_batna must be {name, value}")
    my_r = obj.get("my_reserve")
    their_r = obj.get("their_reserve_estimate")
    if isinstance(my_r, (int, float)) and isinstance(their_r, (int, float)) and their_r < my_r:
        errs.append(f"ZOPA negative (their_reserve {their_r} < my_reserve {my_r})")

    return errs


OK = {   'my_batna': {'name': 'Continue with current vendor at 8K/mo', 'value': 96000},
    'my_reserve': 110000,
    'their_reserve_estimate': 140000,
    'interests': {   'mine': ['predictable cost', 'fast onboarding', 'EU data residency'],
                     'theirs': ['multi-year commitment', 'case study right', 'logo placement']},
    'objective_criteria': [   {   'term': 'annual price',
                                  'benchmark': 'G2 Compete avg 120K',
                                  'source': 'G2 2025 report'}],
    'cialdini_levers': ['reciprocity', 'social-proof']}
BAD = {'my_batna': 'walk away', 'my_reserve': 0}


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
