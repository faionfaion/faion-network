#!/usr/bin/env python3
"""validate-strategy-basics.py — validate the strategy-basics artefact JSON against the output contract.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
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

REQUIRED = ["terms", "last_updated"]


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be an object"]
    for key in REQUIRED:
        if key not in obj:
            errs.append(f"missing required field: {key}")
        elif obj[key] is None or obj[key] == "":
            errs.append(f"required field is empty: {key}")
    return errs


OK = {"terms": [{"term": "mission", "definition": "Why we exist beyond profit.", "example": "ACME exists to make lending accessible to micro-businesses.", "anti_example": "ACME is a bank."}, {"term": "vision", "definition": "Future-state world we aim to create.", "example": "By 2030, every micro-business in the EU can access fair credit in 60s.", "anti_example": "Be number one."}, {"term": "OKR", "definition": "Objective + 3-5 Key Results measurable per cycle.", "example": "Objective: pan-EU expansion. KR1: launch 9 countries by Q4.", "anti_example": "Do better."}, {"term": "SMART", "definition": "Specific, Measurable, Achievable, Relevant, Time-bound.", "example": "Reduce TTM from 180 to 60 days by 2026-Q4.", "anti_example": "Make TTM faster."}, {"term": "strategy_vs_tactics", "definition": "Strategy = choices about where to play and how to win. Tactics = execution moves.", "example": "Strategy: focus on micro-business. Tactic: launch a referral campaign.", "anti_example": "Strategy: launch a referral campaign."}], "last_updated": "2026-05-22"}
BAD = {"terms": []}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: valid fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n")
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
