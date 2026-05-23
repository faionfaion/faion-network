#!/usr/bin/env python3
"""validate-ideation-methods.py

Validate the artefact for the ideation-methods methodology against the schema in
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

REQUIRED = ['method', 'subject', 'output']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    method = obj.get("method")
    out = obj.get("output") or {}
    if method == "scamper":
        for lens in ["substitute", "combine", "adapt", "modify", "put_to_other_use", "eliminate", "reverse"]:
            if not out.get(lens):
                errs.append(f"scamper missing lens: {lens}")

    return errs


OK = {   'method': 'scamper',
    'subject': 'Tip jar in a coffee shop',
    'output': {   'substitute': [   'Replace coins with QR-code tap-to-tip.',
                                    'Replace cash with round-up checkout.'],
                  'combine': ['Combine tip jar with loyalty card stamp.'],
                  'adapt': ['Adapt the tip moment to be photo-friendly for social proof.'],
                  'modify': ['Make the jar transparent + glowing — visible tipping behavior.'],
                  'put_to_other_use': ['Use the jar to collect customer surveys.'],
                  'eliminate': ['Eliminate the jar; add tipping to the receipt screen.'],
                  'reverse': ['Barista tips the customer (rare-find / regular-customer reward).']}}
BAD = {'method': 'scamper', 'subject': 'x', 'output': {'substitute': []}}


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
