#!/usr/bin/env python3
"""validate-freelance-pilot-pricing.py — schema validator. --self-test runs built-in fixtures."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
REQUIRED = ['pilot_id', 'offering', 'customer', 'price', 'cost_basis', 'standard_price', 'timebox_days', 'case_study_consent', 'transition_clause', 'owner']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required: {k}")
    owner = obj.get("owner", "")
    if isinstance(owner, str) and owner:
        if len(owner) < 3 or BANNED.match(owner.strip()):
            errs.append(f"owner invalid: {owner!r}")
    price = obj.get("price")
    cost = obj.get("cost_basis")
    if isinstance(price, (int, float)) and isinstance(cost, (int, float)) and price < cost:
        errs.append("price < cost_basis (rule price-above-cost)")
    tb = obj.get("timebox_days")
    if isinstance(tb, int) and tb > 14:
        errs.append("timebox_days > 14 (rule timebox-14-days)")
    consent = obj.get("case_study_consent") or {}
    if not consent.get("captured_at"):
        errs.append("case_study_consent.captured_at missing (rule case-study-consent-written)")
    tc = obj.get("transition_clause", "")
    if not isinstance(tc, str) or len(tc) < 30:
        errs.append("transition_clause < 30 chars (rule transition-price-documented)")

    return errs


OK = {'pilot_id': 'pp-x', 'offering': 'x', 'customer': 'Acme', 'price': 3500, 'cost_basis': 2800, 'standard_price': 6000, 'timebox_days': 14, 'case_study_consent': {'logo': True, 'metrics': True, 'captured_at': '2026-05-20'}, 'transition_clause': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'owner': '@ruslan'}
BAD = {'pilot_id': 'pp-x', 'price': 100, 'cost_basis': 1000, 'timebox_days': 30, 'owner': 'team', 'offering': 'x', 'customer': 'y', 'standard_price': 6000, 'case_study_consent': {}, 'transition_clause': 'short'}


def self_test():
    if OK and validate(OK):
        sys.stderr.write(f"ok rejected: {validate(OK)}\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str); ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
