#!/usr/bin/env python3
"""validate-modern-ba-framework.py — validate the modern-ba-framework artefact JSON against the output contract.

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

REQUIRED = ["framework", "scores", "rationale", "decided_by", "decided_on"]


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


OK = {"framework": "Hybrid", "scores": {"rigour": 8, "speed": 6, "regulation": 9}, "rationale": "Regulated fintech with weekly delivery cadence; BABOK rigour for compliance artefacts, Lean BA for sprint-level discovery.", "decided_by": "amaia@acme.com", "decided_on": "2026-05-22"}
BAD = {"framework": "Whatever"}


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
