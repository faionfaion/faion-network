#!/usr/bin/env python3
"""validate-freelance-saas-billing-decision.py — schema validator. --self-test runs built-in fixtures."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
REQUIRED = ['decision_id', 'signals', 'options_considered', 'chosen', 'kill_criteria', 'reassessment_at', 'pricing_page_math', 'owner']


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
    pp = obj.get("pricing_page_math", "")
    if not isinstance(pp, str) or len(pp) < 20:
        errs.append("pricing_page_math <20 chars (rule pricing-page-math)")
    chosen = obj.get("chosen")
    kc = obj.get("kill_criteria") or {}
    if chosen and chosen not in kc:
        errs.append(f"kill_criteria.{chosen} missing (rule decision-with-kill-criteria)")
    ra = obj.get("reassessment_at") or {}
    if not isinstance(ra.get("customer_count_threshold"), int) or not isinstance(ra.get("time_window_days"), int):
        errs.append("reassessment_at fields missing (rule reassessment-100-or-6m)")

    return errs


OK = {'decision_id': 'fsb-x', 'signals': {'value_predictability': 'high', 'primary_value_driver': 'per_seat', 'expansion_surface': 'seat_growth', 'customer_size': 'smb'}, 'options_considered': ['subscription', 'usage'], 'chosen': 'subscription', 'kill_criteria': {'subscription': 'if expansion <1.1x in 6m revisit'}, 'reassessment_at': {'customer_count_threshold': 100, 'time_window_days': 180}, 'pricing_page_math': 'Team: $20/seat/month with annual = 2mo free', 'owner': '@ruslan'}
BAD = {'decision_id': 'x', 'owner': 'team', 'chosen': 'subscription', 'pricing_page_math': '$', 'signals': {}, 'options_considered': [], 'kill_criteria': {}, 'reassessment_at': {}}


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
