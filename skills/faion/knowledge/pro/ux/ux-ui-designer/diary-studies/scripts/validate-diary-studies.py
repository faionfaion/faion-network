#!/usr/bin/env python3
"""validate-diary-studies.py

Validate Diary Studies artefact JSON against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['study_id', 'duration_days', 'participants', 'entries', 'themes']


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    return errs


OK = {'study_id': 'sleep-app-q2', 'duration_days': 14, 'participants': [{'id': 'P1', 'segment': 'primary', 'completion_rate': 0.85}, {'id': 'P2', 'segment': 'primary', 'completion_rate': 0.85}, {'id': 'P3', 'segment': 'primary', 'completion_rate': 0.85}, {'id': 'P4', 'segment': 'primary', 'completion_rate': 0.85}, {'id': 'P5', 'segment': 'primary', 'completion_rate': 0.85}, {'id': 'P6', 'segment': 'primary', 'completion_rate': 0.85}, {'id': 'P7', 'segment': 'primary', 'completion_rate': 0.85}, {'id': 'P8', 'segment': 'primary', 'completion_rate': 0.85}], 'entries': [{'participant_id': 'P1', 'timestamp': '2026-05-10T22:30:00Z', 'mode': 'daily', 'context_tag': 'home/bedroom', 'text': 'Used the wind-down routine — fell asleep faster'}], 'themes': [{'theme': 'wind-down routine effectiveness', 'support': 6}, {'theme': 'weekend pattern break', 'support': 5}, {'theme': 'snooze loop', 'support': 4}]}
BAD = {'study_id': 'x'}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
        sys.stderr.write(f"invalid JSON: {e}\n")
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
