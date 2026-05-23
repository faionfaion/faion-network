#!/usr/bin/env python3
"""validate-wcag-22-compliance.py

Validate the artefact for the wcag-22-compliance methodology against the schema in
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

REQUIRED = ['scope', 'sc_results', 'overall_conformance']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    sc = obj.get("sc_results") or {}
    needed = ["2.4.11", "2.4.12", "2.4.13", "2.5.7", "2.5.8", "3.2.6", "3.3.7", "3.3.8", "3.3.9"]
    for k in needed:
        if k not in sc:
            errs.append(f"sc_results missing {k}")
    overall = obj.get("overall_conformance")
    if overall == "AA-2.2-conformant":
        for k, v in sc.items():
            if isinstance(v, dict) and v.get("status") in ("fail", "partial"):
                errs.append(f"claim AA-2.2-conformant but {k} status={v.get('status')}")

    return errs


OK = {   'scope': 'Marketing site v2.0 — 12 page templates + global header/footer',
    'sc_results': {   '2.4.11': {'status': 'pass', 'findings': []},
                      '2.4.12': {'status': 'not-applicable', 'findings': []},
                      '2.4.13': {'status': 'pass', 'findings': []},
                      '2.5.7': {'status': 'pass', 'findings': []},
                      '2.5.8': {   'status': 'partial',
                                   'findings': [   {   'page': '/pricing',
                                                       'issue': 'compare-table checkbox 20×20px'}]},
                      '3.2.6': {'status': 'pass', 'findings': []},
                      '3.3.7': {'status': 'pass', 'findings': []},
                      '3.3.8': {'status': 'pass', 'findings': []},
                      '3.3.9': {'status': 'not-applicable', 'findings': []}},
    'overall_conformance': 'partial'}
BAD = {   'scope': 'x',
    'sc_results': {'2.4.11': {'status': 'pass'}},
    'overall_conformance': 'AA-2.2-conformant'}


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
