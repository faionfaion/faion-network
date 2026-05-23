#!/usr/bin/env python3
"""validate-synthetic-users.py

Validate an artefact for the synthetic-users methodology against the schema in
content/02-output-contract.xml. Stdlib-only.

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

REQUIRED = ["concepts", "synthetic_reactions", "decision_grade", "validation_plan_url", "validation_window_days", "high_stakes_disallowed"]
PLACEHOLDERS = {"tbd", "todo", "fixme", "xxx", "fill_me"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    # placeholder string detection
    def walk(node, path: str):
        if isinstance(node, str):
            if node.strip().lower() in PLACEHOLDERS:
                errs.append(f"placeholder value at {path}: {node!r}")
        elif isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")
    walk(obj, "")
    return errs


OK = json.loads("{\"concepts\": [{\"id\": \"c1\", \"summary\": \"Onboarding cuts to 3 steps\"}, {\"id\": \"c2\", \"summary\": \"Onboarding adds biometric\"}, {\"id\": \"c3\", \"summary\": \"Onboarding offers SSO-only\"}, {\"id\": \"c4\", \"summary\": \"Onboarding offers passkey-only\"}, {\"id\": \"c5\", \"summary\": \"Onboarding deferred to first-action\"}], \"synthetic_reactions\": [{\"concept_id\": \"c1\", \"reaction\": \"Welcome \\u2014 fewer steps reads as professional.\", \"surprise_flag\": false}], \"decision_grade\": false, \"validation_plan_url\": \"https://airtable.com/research-plan-2026-06\", \"validation_window_days\": 21, \"high_stakes_disallowed\": true}")
BAD = json.loads("{\"concepts\": [{\"id\": \"c1\"}], \"decision_grade\": true, \"validation_window_days\": 60}")


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"valid fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
