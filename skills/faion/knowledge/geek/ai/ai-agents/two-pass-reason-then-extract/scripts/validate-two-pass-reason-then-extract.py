#!/usr/bin/env python3
"""validate-two-pass-reason-then-extract.py

Validate the config artefact for the two-pass-reason-then-extract methodology against the schema in
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

REQUIRED = ['pass1_model', 'pass1_thinking', 'pass2_model', 'schema_uri', 'ab_baseline']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'pass1_model': 'claude-opus-4-7', 'pass1_thinking': {'type': 'enabled', 'budget_tokens': 16000}, 'pass2_model': 'claude-haiku-4-7', 'pass2_temperature': 0.0, 'schema_uri': 'schemas/verdict.json', 'transcript_cap_tokens': 8000, 'ab_baseline': {'single_pass_accuracy': 0.74, 'two_pass_accuracy': 0.86, 'delta_pct': 12.0, 'n': 50}}
BAD = {'pass1_model': 'haiku'}


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
