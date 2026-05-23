#!/usr/bin/env python3
"""validate-contextual-inquiry.py

Validate Contextual Inquiry artefact JSON against the schema in 02-output-contract.xml.

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

REQUIRED = ['participants', 'sessions', 'themes']


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    return errs


OK = {'participants': [{'id': 'P1', 'consent_signed': True, 'role': 'nurse'}, {'id': 'P2', 'consent_signed': True, 'role': 'nurse'}, {'id': 'P3', 'consent_signed': True, 'role': 'nurse-manager'}, {'id': 'P4', 'consent_signed': True, 'role': 'tech'}], 'sessions': [{'participant_id': 'P1', 'date': '2026-05-10', 'location_type': 'ward', 'duration_min': 120, 'verbatim_quotes': ["I print the chart because I can't find it on the iPad in time"], 'breakdowns_observed': ['app login times out during rounds']}, {'participant_id': 'P2', 'date': '2026-05-11', 'location_type': 'ward', 'duration_min': 90, 'verbatim_quotes': ['...'], 'breakdowns_observed': ['...']}, {'participant_id': 'P3', 'date': '2026-05-12', 'location_type': 'office', 'duration_min': 60, 'verbatim_quotes': ['...'], 'breakdowns_observed': ['...']}, {'participant_id': 'P4', 'date': '2026-05-13', 'location_type': 'ward', 'duration_min': 90, 'verbatim_quotes': ['...'], 'breakdowns_observed': ['...']}], 'themes': [{'theme': 'session timeout', 'support': 3}, {'theme': 'paper as backup', 'support': 4}, {'theme': 'swipe-to-unlock too slow', 'support': 2}]}
BAD = {'participants': [{'id': 'P1'}]}


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
