#!/usr/bin/env python3
"""validate-data-driven-requirements.py — validate the data-driven-requirements artefact JSON against the output contract.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["requirements", "data_sources", "hypothesis_link"]


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be an object"]
    for key in REQUIRED:
        if key not in obj:
            errs.append(f"missing required field: {key}")
        elif obj[key] is None or obj[key] == "":
            errs.append(f"required field is empty: {key}")
    return errs


OK = {"requirements": [{"req_id": "REQ-DD-001", "statement": "Reduce checkout abandonment on step 3 from 47% to <30%.", "evidence": "GA4 funnel 2026-04, step-3 drop=47% over 12k sessions", "confidence": "high"}], "data_sources": ["ga4://acme/checkout", "sentry://acme/web"], "hypothesis_link": "docs/hypotheses/H-2026-04.md"}
BAD = {"requirements": [{"req_id": "X", "statement": "Make checkout faster"}]}


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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n")
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
