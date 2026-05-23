#!/usr/bin/env python3
"""validate-stakeholder-communication.py

Validate the artefact for the stakeholder-communication methodology against the schema in
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

REQUIRED = ['session_mode', 'stakeholders', 'channel', 'goal']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    sm = obj.get("session_mode")
    if sm not in ["interview", "brainstorm", "clarification", "validation", "socratic"]:
        errs.append(f"session_mode invalid: {sm!r}")
    sts = obj.get("stakeholders") or []
    if not sts:
        errs.append("stakeholders must be non-empty")
    else:
        for s in sts:
            if not all(k in s for k in ("name", "role", "power", "interest")):
                errs.append(f"stakeholder missing power/interest: {s.get('name')!r}")

    return errs


OK = {   'session_mode': 'interview',
    'stakeholders': [   {   'name': 'Anna (VP Eng)',
                            'role': 'decision-maker',
                            'power': 'high',
                            'interest': 'high',
                            'cadence': 'weekly 30 min',
                            'channel_preferred': 'live-video'},
                        {   'name': 'Ben (data-eng lead)',
                            'role': 'implementer',
                            'power': 'low',
                            'interest': 'high',
                            'cadence': 'biweekly async',
                            'channel_preferred': 'async-doc'}],
    'channel': 'live-video',
    'goal': 'Gather requirements for the data-quality dashboard.'}
BAD = {'session_mode': 'everything', 'stakeholders': []}


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
