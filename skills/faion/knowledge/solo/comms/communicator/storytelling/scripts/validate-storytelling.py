#!/usr/bin/env python3
"""validate-storytelling.py

Validate the artefact for the storytelling methodology against the schema in
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

REQUIRED = ['artefact_type', 'framework', 'audience', 'central_claim', 'body']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    fw = obj.get("framework")
    body = obj.get("body") or {}
    if fw == "pixar":
        for k in ("once", "every_day", "one_day", "bot1", "bot2", "until"):
            if not body.get(k):
                errs.append(f"pixar body missing {k}")

    return errs


OK = {   'artefact_type': 'case-study',
    'framework': 'pixar',
    'audience': 'Prospects evaluating SaaS analytics tools',
    'central_claim': 'Acme cut report-generation time from 4 days to 30 minutes by replacing '
                     'manual SQL exports with the analytics platform.',
    'body': {   'once': "Acme's analytics team manually ran weekly SQL exports.",
                'every_day': 'Every Friday morning the senior analyst spent 4 days assembling the '
                             'leadership report.',
                'one_day': 'One Friday the report missed the board meeting; revenue questions went '
                           'unanswered.',
                'bot1': 'Because of that, the CFO mandated an alternative within 2 weeks.',
                'bot2': "Because of that, they evaluated 3 tools and picked Acme's platform.",
                'until': 'Until finally, the same report ran in 30 minutes — and the analyst moved '
                         'to higher-leverage work.'}}
BAD = {'artefact_type': 'case-study', 'framework': 'pyramid', 'body': {'lead': 'stuff happened'}}


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
