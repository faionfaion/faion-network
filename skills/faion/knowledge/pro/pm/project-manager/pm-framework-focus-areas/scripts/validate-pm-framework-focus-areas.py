#!/usr/bin/env python3
"""validate-pm-framework-focus-areas.py

Validate a rubric artefact for PMBoK 8 Focus Areas against the schema in
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

REQUIRED = ['pmbok_version', 'refresh_date', 'matrix']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    import re
    if not re.match(r"^8\.[0-9]+$", str(obj.get("pmbok_version", ""))):
        errs.append(f"pmbok_version pattern invalid: {obj.get('pmbok_version')!r}")
    FA = ["Initiating", "Planning", "Executing",
          "Monitoring and Controlling", "Closing"]
    matrix = obj.get("matrix") or []
    if not isinstance(matrix, list) or len(matrix) != 5:
        errs.append(f"matrix must have exactly 5 focus areas, got {len(matrix)}")
    found = set()
    for row in matrix:
        fa = row.get("focus_area")
        if fa in found:
            errs.append(f"duplicate focus_area: {fa!r}")
        found.add(fa)
        if fa not in FA:
            errs.append(f"focus_area not canonical: {fa!r}")
        domains = row.get("domains") or {}
        for dname, dval in domains.items():
            status = dval.get("status")
            if status == "covered" and not dval.get("artefacts"):
                errs.append(f"matrix.{fa}.{dname} covered but artefacts empty")
            if status == "NA" and not dval.get("na_justification"):
                errs.append(f"matrix.{fa}.{dname} NA without na_justification")
    missing_fa = set(FA) - found
    if missing_fa:
        errs.append(f"matrix missing focus areas: {sorted(missing_fa)}")

    return errs


GOOD = {'pmbok_version': '8.0', 'refresh_date': '2026-05-22', 'matrix': [{'focus_area': 'Initiating', 'domains': {'Stakeholder': {'status': 'covered', 'artefacts': ['x']}}}, {'focus_area': 'Planning', 'domains': {'Stakeholder': {'status': 'covered', 'artefacts': ['x']}}}, {'focus_area': 'Executing', 'domains': {'Stakeholder': {'status': 'covered', 'artefacts': ['x']}}}, {'focus_area': 'Monitoring and Controlling', 'domains': {'Stakeholder': {'status': 'covered', 'artefacts': ['x']}}}, {'focus_area': 'Closing', 'domains': {'Stakeholder': {'status': 'covered', 'artefacts': ['x']}}}]}
BAD = {'pmbok_version': '7', 'refresh_date': 'y', 'matrix': [{'focus_area': 'Initiating', 'domains': {}}]}


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
