#!/usr/bin/env python3
"""validate-performance-domains-overview.py

Validate a rubric artefact for PMBoK Performance Domains Overview against the schema in
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

REQUIRED = ['project_id', 'scorer', 'scored_at', 'domains']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    EIGHT = {"stakeholder", "team", "development_approach", "planning",
             "project_work", "delivery", "measurement", "uncertainty"}
    domains = obj.get("domains") or {}
    missing = EIGHT - set(domains.keys())
    if missing:
        errs.append(f"domains missing: {sorted(missing)}")
    for k, v in domains.items():
        if not isinstance(v, dict):
            errs.append(f"domains.{k} must be object"); continue
        score = v.get("score")
        if score not in {"red", "amber", "green"}:
            errs.append(f"domains.{k}.score invalid: {score!r}")
        if not v.get("evidence"):
            errs.append(f"domains.{k}.evidence empty")
        if score in {"red", "amber"} and not v.get("recommended_action"):
            errs.append(f"domains.{k} amber/red without recommended_action")

    return errs


GOOD = {'project_id': 'acme', 'scorer': 'U_PMO', 'scored_at': '2026-05-22', 'domains': {'stakeholder': {'score': 'green', 'evidence': ['e1']}, 'team': {'score': 'green', 'evidence': ['e1']}, 'development_approach': {'score': 'green', 'evidence': ['e1']}, 'planning': {'score': 'green', 'evidence': ['e1']}, 'project_work': {'score': 'green', 'evidence': ['e1']}, 'delivery': {'score': 'green', 'evidence': ['e1']}, 'measurement': {'score': 'green', 'evidence': ['e1']}, 'uncertainty': {'score': 'green', 'evidence': ['e1']}}}
BAD = {'project_id': 'x', 'scorer': '', 'scored_at': 'y', 'domains': {'stakeholder': {'score': 'ok'}}}


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
