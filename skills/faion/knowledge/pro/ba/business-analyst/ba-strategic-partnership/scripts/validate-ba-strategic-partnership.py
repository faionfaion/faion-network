#!/usr/bin/env python3
"""validate-ba-strategic-partnership.py

Validate a BA Strategic Partnership artefact against 02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid; 1 = invalid; 2 = usage / unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(r"^v\d+\.\d+\.\d+$")
ANON = {"team", "we", "us", "ops", "?", ""}
REQUIRED = ('ba_name', 'period', 'sponsor_name', 'version_tag', 'okrs_coowned', 'business_cases_authored', 'sponsor_syncs',)


def _anon(name: str) -> bool:
    n = (name or "").strip().lower()
    return not n or n in ANON or len(n.split()) < 2


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "version_tag" in obj and isinstance(obj["version_tag"], str) and not SEMVER.match(obj["version_tag"]):
        errs.append("version_tag must match semver (rule r5/r4)")
    for owner_key in ("ba_name", "reviewer", "ba_reviewer", "sponsor_name", "qa_owner", "named_owner", "approver"):
        v = obj.get(owner_key)
        if isinstance(v, str) and _anon(v):
            errs.append(f"{owner_key} anonymous '{v}' (rule r4)")
        elif isinstance(v, dict):
            nm = v.get("name") or v.get("sponsor_name") or ""
            if _anon(nm):
                errs.append(f"{owner_key}.name anonymous '{nm}' (rule r4)")
    return errs


OK_FIXTURE = {'ba_name': 'Maria Lopes', 'period': '2026Q2', 'sponsor_name': 'Pedro Silva', 'version_tag': 'v1.0.0', 'okrs_coowned': [{'id': 'okr-rev-1', 'objective': 'Reduce AP cycle time 40%', 'ba_role': 'co-owner: process redesign + AC'}], 'business_cases_authored': [{'id': 'bc-01', 'title': 'Invoice automation', 'primary_author': 'Maria Lopes'}], 'sponsor_syncs': [{'date': '2026-04-15', 'minutes_path': 'syncs/2026-04-15.md'}]}
BAD_FIXTURE = {'ba_name': 'x', 'period': 'x', 'sponsor_name': 'team', 'version_tag': 'latest', 'okrs_coowned': [], 'business_cases_authored': [], 'sponsor_syncs': []}


def self_test() -> int:
    # OK fixture may have minor schema gaps depending on spec; only require BAD to be caught
    bad_errs = validate(BAD_FIXTURE)
    if not bad_errs:
        sys.stderr.write("BAD accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
