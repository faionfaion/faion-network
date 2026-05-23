#!/usr/bin/env python3
"""validate-market-sizing-with-ai.py

Validate the artefact produced by the market-sizing-with-ai methodology against the
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

REQUIRED = ['market_definition', 'year_horizon', 'currency', 'top_down', 'bottom_up', 'value_theory', 'reconciliation', 'citations']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'market_definition': 'AI coding-agent tools for solo developers, 2026, North America + EU', 'year_horizon': 2026, 'currency': 'USD', 'top_down': {'value': 8200000000.0, 'rationale': 'AI dev tools market $40B × 20% coding-agent share'}, 'bottom_up': {'value': 5400000000.0, 'rationale': '18M solo devs × $25/mo ARPU × 100% addressable'}, 'value_theory': {'value': 6800000000.0, 'rationale': 'Time saved $500/dev/yr × 18M × 75% capture'}, 'reconciliation': 'Spread 1.5x; top-down skews high due to bundled dev-tool revenue; bottom-up conservative ARPU; value-theory mid-point. Plan on $6B central estimate.', 'citations': [{'url': 'https://example.com/r1', 'year': 2026, 'claim': 'AI dev tools market $40B'}, {'url': 'https://example.com/r2', 'year': 2025, 'claim': 'Coding-agent share 20%'}, {'url': 'https://example.com/r3', 'year': 2026, 'claim': 'Solo developer population 18M'}]}
BAD = {'market_definition': 'tam'}


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
