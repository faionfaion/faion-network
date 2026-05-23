#!/usr/bin/env python3
"""validate-cognitive-inclusion-design.py

Validate Cognitive Inclusion Design artefact JSON against the schema in 02-output-contract.xml.

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

REQUIRED = ['surface', 'patterns', 'settings', 'wcag_mapping']


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    return errs


OK = {'surface': 'loan-application-flow', 'patterns': {'chunking': '5 steps of <=4 fields each', 'predictability': 'labels match destination, stable nav', 'escape_hatch': 'Save and exit available on every step'}, 'settings': {'focus_mode': 'hides side-rail', 'dyslexia_font': 'OpenDyslexic toggle', 'reduced_motion': 'respects OS + in-product override', 'extended_time': '+50% on all timers', 'plain_language': 'Grade 5-6 toggle'}, 'wcag_mapping': [{'sc': '2.4.8', 'pattern': 'chunking'}, {'sc': '3.2.4', 'pattern': 'predictability'}, {'sc': '2.2.1', 'pattern': 'extended_time'}]}
BAD = {'surface': 'x'}


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
