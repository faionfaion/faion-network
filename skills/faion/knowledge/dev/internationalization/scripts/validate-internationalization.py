#!/usr/bin/env python3
"""validate-internationalization.py

Validate the artefact for the internationalization methodology against the JSON Schema
in content/02-output-contract.xml.

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

REQUIRED = ["catalogue_path", "locales_count", "keys_count", "hardcoded_strings", "physical_css_props", "pseudo_loc_in_ci"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'locales_count' in obj and (not isinstance(obj['locales_count'], int) or obj['locales_count'] < 2):
        errs.append('locales_count must be int >= 2')
    if 'keys_count' in obj and (not isinstance(obj['keys_count'], int) or obj['keys_count'] < 1):
        errs.append('keys_count must be int >= 1')
    if 'catalogue_path' in obj and (not isinstance(obj['catalogue_path'], str) or len(obj['catalogue_path']) < 3):
        errs.append('catalogue_path must be >= 3 chars')
    if 'hardcoded_strings' in obj and obj['hardcoded_strings'] != 0:
        errs.append('hardcoded_strings must be 0')
    return errs


OK = {'catalogue_path': 'locales/', 'locales_count': 4, 'keys_count': 312, 'hardcoded_strings': 0, 'physical_css_props': 2, 'pseudo_loc_in_ci': True, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'catalogue_path': 'x', 'locales_count': 1, 'hardcoded_strings': 14, 'pseudo_loc_in_ci': False}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
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
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
