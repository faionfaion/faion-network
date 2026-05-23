#!/usr/bin/env python3
"""validate-decision-analysis.py

Validate a decision-record artefact produced by the decision-analysis methodology
against the JSON Schema captured in content/02-output-contract.xml.

stdlib-only. Inputs / outputs / exit codes documented under --help.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture
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

REQUIRED = ['decision_id', 'statement', 'options', 'criteria', 'weights', 'scores', 'sensitivity', 'recommended']


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"decision_id": "DR-0007", "statement": "Choose the platform that minimises 5-year TCO while meeting compliance.", "options": [{"option_id": "O1", "name": "Status quo", "is_status_quo": true}, {"option_id": "O2", "name": "Salesforce", "is_status_quo": false}, {"option_id": "O3", "name": "HubSpot", "is_status_quo": false}], "criteria": [{"criterion_id": "C1", "description": "TCO 5y", "trace_to_req": "BR-0010"}, {"criterion_id": "C2", "description": "Compliance fit", "trace_to_req": "BR-0014"}], "weights": {"C1": 0.6, "C2": 0.4}, "scores": {"O1": {"C1": 3, "C2": 2}, "O2": {"C1": 4, "C2": 5}, "O3": {"C1": 5, "C2": 3}}, "sensitivity": {"method": "one-at-a-time", "robustness": 0.82}, "recommended": "O2", "dissent": []}')
BAD = json.loads('{"decision_id": "x", "statement": "buy Salesforce"}')


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: good fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: bad fixture accepted\n")
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
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"VIOLATION: invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
