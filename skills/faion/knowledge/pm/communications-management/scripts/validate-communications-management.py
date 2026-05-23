#!/usr/bin/env python3
"""validate-communications-management.py

Validate a spec artefact for Communications Management against the schema in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    path to artefact JSON
    --self-test    run built-in fixtures and exit
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['project_id', 'comms_matrix', 'decision_log_pointer', 'meeting_cadence']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    matrix = obj.get("comms_matrix") or []
    if not isinstance(matrix, list) or not matrix:
        errs.append("comms_matrix must be non-empty list")
    else:
        for i, row in enumerate(matrix):
            for k in ("stakeholder", "artefact", "channel", "owner", "cadence",
                      "format", "escalation"):
                if k not in row:
                    errs.append(f"comms_matrix[{i}].{k} missing")
    if not obj.get("decision_log_pointer"):
        errs.append("decision_log_pointer must be non-empty")
    cadence = obj.get("meeting_cadence") or []
    if not isinstance(cadence, list):
        errs.append("meeting_cadence must be list")

    return errs


GOOD = {'project_id': 'acme', 'comms_matrix': [{'stakeholder': 'sponsor', 'artefact': 'status', 'channel': 'email', 'owner': 'U_PM', 'cadence': 'weekly', 'format': 'md', 'escalation': 'U_HEAD'}], 'decision_log_pointer': './decision-log.md', 'meeting_cadence': [{'meeting': 'weekly', 'cadence': 'weekly', 'owner': 'U_PM'}]}
BAD = {'project_id': 'x', 'comms_matrix': [], 'decision_log_pointer': '', 'meeting_cadence': []}


def self_test():
    if validate(GOOD):
        sys.stderr.write("good rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
        sys.stderr.write(f"JSON parse error: {e}\n"); return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
