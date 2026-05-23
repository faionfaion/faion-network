#!/usr/bin/env python3
"""validate-difficult-conversations.py

Validate the artefact for the difficult-conversations methodology against the schema in
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

REQUIRED = ['format', 'fact', 'story', 'state_or_desc', 'wwwf']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    fmt = obj.get("format")
    if fmt not in ["state", "desc"]:
        errs.append(f"format must be state or desc, got {fmt!r}")
    wwwf = obj.get("wwwf") or {}
    for k in ("who", "what", "when", "follow_up"):
        if not wwwf.get(k):
            errs.append(f"wwwf missing {k}")

    return errs


OK = {   'format': 'state',
    'fact': 'The last three milestones were delivered 2-3 days late.',
    'story': "I am starting to worry about whether we'll hit the launch date.",
    'state_or_desc': {   'share_facts': 'The last three milestones were delivered 2-3 days late.',
                         'tell_story': "I'm starting to worry about whether we'll hit the launch "
                                       'date.',
                         'ask_path': "Can you help me understand what's happening?",
                         'talk_tentative': 'I might be missing context.',
                         'encourage_test': "I'm open to hearing I'm wrong about this."},
    'wwwf': {   'who': 'owner-A',
                'what': 'circulate revised milestone plan',
                'when': 'Friday EOD',
                'follow_up': 'Tuesday 11:00 review'}}
BAD = {'format': 'state', 'fact': "you don't care", 'story': 'stuff'}


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
