#!/usr/bin/env python3
# purpose: validate vision-accessibility JSON artefact against 02-output-contract schema
# consumes: JSON file passed via --file
# produces: exit-code 0 (valid) or 1 (invalid + violations on stderr)
# depends-on: stdlib only (argparse + json + re + pathlib)
# token-budget-impact: 0 (out-of-band)
"""validate-vision-accessibility.py — validate a vision-accessibility JSON artefact.

Inputs:
    --file PATH    JSON file to validate
    --self-test    run built-in valid + invalid fixtures
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

REQUIRED = ['artefact_id', 'image_url', 'alt_text', 'long_description', 'is_decorative', 'contains_text']

TYPE_MAP = {
    'artefact_id': 'string',
    'image_url': 'string',
    'alt_text': 'string',
    'long_description': 'string',
    'is_decorative': 'boolean',
    'contains_text': 'boolean',
    'text_content': 'string',
    'chart_insight': 'string',
}

PYTHON_TYPES = {
    "string": str, "integer": int, "number": (int, float),
    "boolean": bool, "array": list, "object": dict,
}

def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        expected = PYTHON_TYPES.get(TYPE_MAP.get(k, "string"), str)
        if not isinstance(obj[k], expected):
            errs.append(f"field {k} must be {TYPE_MAP.get(k)}, got {type(obj[k]).__name__}")
    return errs

VALID_FIX = {
    'artefact_id': 'x',
    'image_url': 'x',
    'alt_text': 'x',
    'long_description': 'x',
    'is_decorative': True,
    'contains_text': True,
    'text_content': 'x',
    'chart_insight': 'x',
}
INVALID_FIX = {}

def self_test():
    if validate(VALID_FIX):
        sys.stderr.write("valid fixture rejected\n"); return 1
    if not validate(INVALID_FIX):
        sys.stderr.write("invalid fixture accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"json parse: {e}\n"); return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0

if __name__ == "__main__":
    sys.exit(main())
