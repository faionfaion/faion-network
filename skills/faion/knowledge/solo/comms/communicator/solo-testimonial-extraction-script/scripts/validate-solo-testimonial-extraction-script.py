#!/usr/bin/env python3
"""validate-solo-testimonial-extraction-script.py

Validate the artefact for the solo-testimonial-extraction-script methodology against the schema in
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

REQUIRED = ['customer', 'hesitation', 'outcome', 'anti_recommendation', 'metric', 'consent']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    metric = obj.get("metric") or ""
    if not any(c.isdigit() for c in metric):
        errs.append("metric must contain a number")
    consent = obj.get("consent") or {}
    for k in ("quote", "name", "logo"):
        if k not in consent:
            errs.append(f"consent missing {k}")

    return errs


OK = {   'customer': {'name': 'Maria K.', 'role': 'Founder', 'company': 'ShopGrow'},
    'hesitation': "I worried it would be another tool I'd never set up.",
    'outcome': 'Inventory close went from 4 hours every Monday to 20 minutes.',
    'anti_recommendation': "Not for solo founders with fewer than 50 SKUs — the setup payoff isn't "
                           'there yet.',
    'metric': '3.5h saved per week (~14h/month).',
    'consent': {'quote': True, 'name': True, 'logo': False},
    'verbatim_marker': True}
BAD = {'customer': {'name': 'x'}, 'hesitation': 'good'}


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
