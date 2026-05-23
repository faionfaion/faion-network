#!/usr/bin/env python3
"""validate-freelancer-discovery-call-template.py

Validate the artefact for the freelancer-discovery-call-template methodology against the schema in
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

REQUIRED = ['prospect', 'sections', 'scorecard', 'proposal_seed']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    sec = obj.get("sections") or {}
    for k in ("context", "pain", "success_criteria", "budget_signals", "decision_process"):
        if k not in sec:
            errs.append(f"sections missing {k}")
    sc = obj.get("scorecard") or {}
    total = sc.get("total")
    if isinstance(total, int) and total > 25:
        errs.append(f"scorecard.total > 25: {total}")
    share = obj.get("operator_word_share")
    if isinstance(share, (int, float)) and share > 0.30:
        errs.append(f"operator_word_share > 0.30: {share}")

    return errs


OK = {   'prospect': {'name': 'Carlos R.', 'company': 'BrewLab', 'role': 'Founder'},
    'sections': {   'context': [   'Walk me through what your team does today.',
                                   'How did you find me?'],
                    'pain': [   "What's slowing you down most this quarter?",
                                'Tell me about the last time it broke.'],
                    'success_criteria': [   "What would 'done' look like in 90 days?",
                                            'How will you measure it?'],
                    'budget_signals': [   'What are you spending on this today?',
                                          'What budget have you allocated?'],
                    'decision_process': ['Who else weighs in?', "What's your timeline to start?"]},
    'scorecard': {   'fit': 4,
                     'urgency': 4,
                     'budget': 3,
                     'decision_power': 5,
                     'vibes': 4,
                     'total': 20},
    'proposal_seed': {   'problem': 'BrewLab loses 6h/week reconciling SKU spreadsheets.',
                         'approach': 'Replace manual reconciliation with Airtable + automation; 2 '
                                     'weeks build.',
                         'scope': 'Setup, data migration, 2 trainings.',
                         'price': '€4,500 fixed.',
                         'timeline': 'Start within 2 weeks; deliver 14 days; 30-day post-launch '
                                     'support.'},
    'operator_word_share': 0.22}
BAD = {'prospect': {'name': 'x'}, 'sections': {}, 'scorecard': {'total': 30}}


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
