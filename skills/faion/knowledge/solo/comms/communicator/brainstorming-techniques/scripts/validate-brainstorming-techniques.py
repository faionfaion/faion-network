#!/usr/bin/env python3
"""validate-brainstorming-techniques.py

Validate the artefact for the brainstorming-techniques methodology against the schema in
02-output-contract.xml.

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

REQUIRED = ['problem', 'technique', 'participants', 'quantity_target', 'session_plan', 'scored_shortlist']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    sl = obj.get("scored_shortlist") or []
    if not isinstance(sl, list) or len(sl) < 5:
        errs.append("scored_shortlist must be list of >=5")
    technique = obj.get("technique")
    if technique not in ["classic", "brainwriting-6-3-5", "round-robin", "reverse"]:
        errs.append(f"unsupported technique: {technique!r}")

    return errs


OK = {   'problem': 'How might we reduce new-user activation time from 12 min to <5 min?',
    'technique': 'brainwriting-6-3-5',
    'participants': ['PM', 'designer-1', 'designer-2', 'engineer-1', 'engineer-2', 'ops'],
    'quantity_target': 90,
    'session_plan': {   'duration_min': 35,
                        'phases': [   'intro (5)',
                                      '6 rounds of 6-3-5 (24)',
                                      'dedup-cluster (4)',
                                      'score (2)']},
    'scored_shortlist': [   {   'idea': 'Skip account-create; start with magic-link onboarding',
                                'cluster': 'auth-flow',
                                'impact': 5,
                                'effort': 3},
                            {   'idea': 'Default demo data on first login',
                                'cluster': 'first-run',
                                'impact': 4,
                                'effort': 2},
                            {   'idea': 'Tour video <90s embedded on dashboard',
                                'cluster': 'education',
                                'impact': 3,
                                'effort': 2},
                            {   'idea': 'Progressive disclosure of advanced settings',
                                'cluster': 'ui',
                                'impact': 4,
                                'effort': 4},
                            {   'idea': 'Sample template gallery',
                                'cluster': 'first-run',
                                'impact': 3,
                                'effort': 3}]}
BAD = {'problem': 'ideas?', 'technique': 'freeform'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"ok rejected: {errs_ok}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
