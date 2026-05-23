#!/usr/bin/env python3
"""validate-puppeteer-launch-setup.py

Validate the config artefact for the puppeteer-launch-setup methodology against the JSON Schema
defined in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['env', 'sandbox_flags_set', 'chromium_pinned', 'cache_dir_set', 'close_in_finally', 'default_wait_until']


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'env': 'ci', 'sandbox_flags_set': True, 'chromium_pinned': True, 'cache_dir_set': True, 'close_in_finally': True, 'default_wait_until': 'domcontentloaded', 'default_timeout_ms': 20000}
BAD = {'env': 'docker', 'sandbox_flags_set': False, 'chromium_pinned': False, 'close_in_finally': False, 'default_wait_until': 'networkidle0'}


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
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
