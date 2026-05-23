#!/usr/bin/env python3
"""validate-cross-platform-token-distribution.py

Validate Cross-Platform Token Distribution artefact JSON against the schema in 02-output-contract.xml.

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

REQUIRED = ['source', 'platforms', 'transforms']


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    return errs


OK = {'source': 'tokens.json', 'platforms': ['web-css', 'ios-swift', 'android-xml', 'tailwind'], 'transforms': [{'platform': 'web-css', 'transform': 'css-variables', 'output_path': 'dist/web/tokens.css'}, {'platform': 'ios-swift', 'transform': 'ios-swift-class', 'output_path': 'dist/ios/Tokens.swift'}, {'platform': 'android-xml', 'transform': 'android-color-resource', 'output_path': 'dist/android/colors.xml'}, {'platform': 'tailwind', 'transform': 'tailwind-config', 'output_path': 'dist/web/tailwind.config.js'}]}
BAD = {'source': 'x'}


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
