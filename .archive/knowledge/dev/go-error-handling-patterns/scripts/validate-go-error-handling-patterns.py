#!/usr/bin/env python3
"""validate-go-error-handling-patterns.py

Validate the artefact for the go-error-handling-patterns methodology against the JSON Schema
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

REQUIRED = ["apperror_package", "sentinel_count", "unwrapped_boundaries", "type_assertion_count", "edge_translator_count", "control_flow_panics"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'sentinel_count' in obj and (not isinstance(obj['sentinel_count'], int) or obj['sentinel_count'] < 1):
        errs.append('sentinel_count must be int >= 1')
    if 'apperror_package' in obj and (not isinstance(obj['apperror_package'], str) or len(obj['apperror_package']) < 3):
        errs.append('apperror_package must be >= 3 chars')
    if 'unwrapped_boundaries' in obj and obj['unwrapped_boundaries'] != 0:
        errs.append('unwrapped_boundaries must be 0')
    if 'type_assertion_count' in obj and obj['type_assertion_count'] != 0:
        errs.append('type_assertion_count must be 0')
    if 'edge_translator_count' in obj and obj['edge_translator_count'] != 1:
        errs.append('edge_translator_count must be exactly 1')
    if 'control_flow_panics' in obj and obj['control_flow_panics'] != 0:
        errs.append('control_flow_panics must be 0')
    return errs


OK = {'apperror_package': 'internal/apperror', 'sentinel_count': 5, 'unwrapped_boundaries': 0, 'type_assertion_count': 0, 'edge_translator_count': 1, 'control_flow_panics': 0, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'apperror_package': 'x', 'sentinel_count': 0, 'unwrapped_boundaries': 4, 'type_assertion_count': 7, 'edge_translator_count': 3}


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
