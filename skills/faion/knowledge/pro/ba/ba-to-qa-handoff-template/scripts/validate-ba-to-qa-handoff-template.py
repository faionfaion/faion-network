#!/usr/bin/env python3
"""validate-ba-to-qa-handoff-template.py

Validate a BA to QA Handoff artefact against 02-output-contract.xml.

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
REQUIRED = ('handoff_id', 'version', 'story_id', 'acceptance_criteria_count', 'fixtures', 'edge_cases', 'qa_owner', 'ba_signoff_ts',)


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
    if "owner" in obj or "named_owner" in obj:
        own = obj.get("owner") or obj.get("named_owner") or obj.get("approver", {}).get("name") or ""
        if isinstance(own, str) and _anon(own):
            errs.append(f"owner anonymous '{own}' (rule r3)")
    if "version" in obj and not SEMVER.match(obj.get("version", "")):
        errs.append("version must match semver (rule r4)")
    return errs


OK_FIXTURE = {'version': 'v1.0.0', 'handoff_id': 'h-1', 'story_id': 'STORY-101', 'acceptance_criteria_count': 5, 'fixtures': ['fix/happy.json'], 'edge_cases': ['empty cart'], 'qa_owner': 'Inês Costa', 'ba_signoff_ts': '2026-05-23T14:00:00Z'}
BAD_FIXTURE = {}


def self_test() -> int:
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
