#!/usr/bin/env python3
"""validate-logging-patterns.py

Validate the artefact for the logging-patterns methodology against the JSON Schema
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

REQUIRED = ["logger_module", "json_output", "correlation_id_middleware", "redaction_pipeline_count", "pii_field_count", "print_calls"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'logger_module' in obj and (not isinstance(obj['logger_module'], str) or len(obj['logger_module']) < 3):
        errs.append('logger_module must be >= 3 chars')
    if 'redaction_pipeline_count' in obj and obj['redaction_pipeline_count'] != 1:
        errs.append('redaction_pipeline_count must be exactly 1')
    if 'print_calls' in obj and obj['print_calls'] != 0:
        errs.append('print_calls must be 0')
    if 'pii_field_count' in obj and (not isinstance(obj['pii_field_count'], int) or obj['pii_field_count'] < 1):
        errs.append('pii_field_count must be int >= 1')
    return errs


OK = {'logger_module': 'app.observability.logger', 'json_output': True, 'correlation_id_middleware': True, 'redaction_pipeline_count': 1, 'pii_field_count': 8, 'print_calls': 0, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'logger_module': 'x', 'json_output': False, 'redaction_pipeline_count': 4, 'print_calls': 17}


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
