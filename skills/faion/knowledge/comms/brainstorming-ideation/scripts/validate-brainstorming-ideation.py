#!/usr/bin/env python3
"""validate-brainstorming-ideation.py

Validate the artefact for the brainstorming-ideation methodology against the schema in
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

REQUIRED = ['problem', 'personas', 'raw_count', 'shortlist']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    personas = obj.get("personas") or []
    if not isinstance(personas, list) or len(personas) < 3:
        errs.append("personas must be list of >=3")
    if (obj.get("raw_count") or 0) < 30:
        errs.append("raw_count must be >=30")
    sl = obj.get("shortlist") or []
    if not isinstance(sl, list) or len(sl) < 5:
        errs.append("shortlist must be list of >=5")
    else:
        for item in sl:
            if "provenance" not in item:
                errs.append(f"shortlist item missing provenance: {item.get('idea')!r}")

    return errs


OK = {   'problem': 'How might we reduce email response time for support inbox below 1h median?',
    'personas': ['solo-founder', 'small-team-lead', 'support-agent'],
    'raw_count': 78,
    'shortlist': [   {   'idea': 'Tag-routed canned-reply library',
                         'cluster': 'templates',
                         'impact': 5,
                         'effort': 2,
                         'provenance': {'persona': 'solo-founder', 'branch': 'classic'}},
                     {   'idea': 'Triage bot tags ticket priority',
                         'cluster': 'triage',
                         'impact': 4,
                         'effort': 3,
                         'provenance': {'persona': 'small-team-lead', 'branch': 'classic'}},
                     {   'idea': 'Auto-close stale low-priority threads',
                         'cluster': 'triage',
                         'impact': 3,
                         'effort': 1,
                         'provenance': {'persona': 'support-agent', 'branch': 'reverse'}},
                     {   'idea': 'Office-hours boundary on email signature',
                         'cluster': 'expectations',
                         'impact': 3,
                         'effort': 1,
                         'provenance': {'persona': 'solo-founder', 'branch': 'classic'}},
                     {   'idea': 'Daily 30-min sweep block on calendar',
                         'cluster': 'process',
                         'impact': 4,
                         'effort': 1,
                         'provenance': {'persona': 'solo-founder', 'branch': 'classic'}}]}
BAD = {'problem': 'x', 'shortlist': []}


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
