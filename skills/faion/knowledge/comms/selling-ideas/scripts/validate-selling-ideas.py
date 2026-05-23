#!/usr/bin/env python3
"""validate-selling-ideas.py

Validate the artefact for the selling-ideas methodology against the schema in
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

REQUIRED = ['format', 'audience', 'challenger_insight', 'spin', 'cta']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    spin = obj.get("spin") or {}
    for k in ("situation", "problem", "implication", "need_payoff"):
        if not spin.get(k):
            errs.append(f"spin missing {k}")
    cta = (obj.get("cta") or "").lower()
    if "let me know" in cta or "whenever" in cta:
        errs.append("cta is vague ('let me know' / 'whenever')")

    return errs


OK = {   'format': 'executive',
    'audience': 'CTO at Series-B SaaS',
    'challenger_insight': 'Most teams assume incident response is a tools problem; data shows 70% '
                          'of MTTR is the human handoff between detection and ownership.',
    'spin': {   'situation': 'Your on-call is 3 engineers rotating weekly.',
                'problem': 'Sev-2 incidents take 40 minutes from page to active ownership.',
                'implication': "At your scale that's ~8h/month of latent customer impact + 1 "
                               'escalation/month to your phone.',
                'need_payoff': 'If we cut handoff latency to 5 min, you reclaim 7h/month of '
                               'on-call energy and 90% of those escalations.'},
    'cta': 'Can we schedule a 30-min architecture review next Thursday?'}
BAD = {'format': 'elevator', 'spin': {'need_payoff': 'buy us!'}, 'cta': 'let me know'}


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
