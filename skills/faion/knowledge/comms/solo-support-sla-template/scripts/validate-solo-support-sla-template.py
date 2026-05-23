#!/usr/bin/env python3
"""validate-solo-support-sla-template.py

Validate the artefact for the solo-support-sla-template methodology against the schema in
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

REQUIRED = ['tiers', 'business_hours', 'canned_replies', 'escalation_trigger']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    tiers = obj.get("tiers") or []
    if len(tiers) != 3:
        errs.append(f"tiers must be exactly 3, got {len(tiers)}")
    cr = obj.get("canned_replies") or []
    if len(cr) < 4:
        errs.append(f"canned_replies must be >=4, got {len(cr)}")

    return errs


OK = {   'tiers': [   {'name': 'community', 'response_time_h': 72, 'channels': ['email', 'discord']},
                 {'name': 'paid', 'response_time_h': 24, 'channels': ['email', 'in-app']},
                 {   'name': 'enterprise',
                     'response_time_h': 4,
                     'channels': ['email', 'in-app', 'slack']}],
    'business_hours': {   'timezone': 'Europe/Lisbon',
                          'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                          'start': '09:00',
                          'end': '18:00'},
    'canned_replies': [   {'key': 'ack', 'body': "Got it — I'll reply within SLA."},
                          {'key': 'deflect', 'body': 'This is covered in docs at <URL>.'},
                          {'key': 'escalate', 'body': 'Escalating to operator phone.'},
                          {   'key': 'after-hours',
                              'body': 'Outside business hours; replying first thing tomorrow.'}],
    'escalation_trigger': 'Paying customer with 0 reply 48h after first message auto-escalates to '
                          'operator phone.'}
BAD = {'tiers': [{'name': 'premium', 'response_time_h': 1}], 'business_hours': {}}


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
