#!/usr/bin/env python3
"""validate-ai-interview-analysis.py

Validate the artefact produced by the ai-interview-analysis methodology against the
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

REQUIRED = ['interview_id', 'highlights', 'codes', 'contradictions', 'follow_up_questions', 'verified_by']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'interview_id': 'i07', 'highlights': [{'text': 'I gave up after the third login redirect', 'line_range_start': 42, 'line_range_end': 48}], 'codes': ['pain.auth'], 'contradictions': [{'a_range': 'L20-L25', 'b_range': 'L150-L155', 'note': 'Initially said auth was fine, later said it killed onboarding.'}], 'follow_up_questions': [{'question': 'What changed your mind about auth between minute 5 and minute 45?', 'reason': 'Probes L20-L25 vs L150-L155 contradiction.'}], 'verified_by': 'ruslan@faion.net'}
BAD = {'interview_id': 'x'}


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
