#!/usr/bin/env python3
"""validate-conflict-resolution.py

Validate the artefact for the conflict-resolution methodology against the schema in
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

REQUIRED = ['tk_mode', 'observation', 'feeling', 'need', 'request']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    feeling = obj.get("feeling") or ""
    if not feeling.startswith("I feel "):
        errs.append("feeling must start with 'I feel '")
    request = obj.get("request") or ""
    if request.lower().startswith("stop ") or request.lower().startswith("don't "):
        errs.append("request must be positively framed, not 'stop X' / 'don't X'")

    return errs


OK = {   'tk_mode': 'collaborating',
    'observation': 'In the last 3 sprints the deploy ticket I assigned was returned without '
                   'comments 14h after the SLA.',
    'feeling': 'I feel frustrated and uncertain about how to plan next sprint.',
    'need': 'predictability and clarity on shared deliverables',
    'request': 'Would you commit to a 4h response window during business hours starting next '
               'Monday, or propose an alternative we both agree to by Friday?'}
BAD = {'tk_mode': 'fight', 'observation': 'you are unreliable', 'feeling': 'you upset me'}


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
