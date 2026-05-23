#!/usr/bin/env python3
"""validate-freelance-referral-program-design.py — schema validator. --self-test runs built-in fixtures."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
REQUIRED = ['program_id', 'incentive', 'attribution_window_days', 'referrers', 'partners', 'testimonial_framing', 'owner']


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
    inc = obj.get("incentive") or {}
    if inc.get("type") not in {"flat_cash", "credit"}:
        errs.append("incentive.type must be flat_cash/credit (rule flat-incentive-not-percent)")
    aw = obj.get("attribution_window_days")
    if isinstance(aw, int) and aw > 90:
        errs.append("attribution_window_days > 90 (rule attribution-window-90-days)")
    for i, r in enumerate(obj.get("referrers") or []):
        if not r.get("written_terms_date"):
            errs.append(f"referrers[{i}].written_terms_date missing (rule written-incentive-per-referrer)")
    for i, p in enumerate(obj.get("partners") or []):
        if not p.get("swap_opt_in_date"):
            errs.append(f"partners[{i}].swap_opt_in_date missing (rule partner-swap-opted-in)")
    tf = obj.get("testimonial_framing") or {}
    if not tf.get("template") or not tf.get("approved_by_customers"):
        errs.append("testimonial_framing missing fields (rule nda-safe-testimonial-framing)")

    return errs


OK = {'program_id': 'frp-1', 'incentive': {'type': 'flat_cash', 'amount_usd': 500}, 'attribution_window_days': 90, 'referrers': [{'handle': '@x', 'written_terms_date': '2026-05-10'}], 'partners': [{'handle': '@y', 'swap_opt_in_date': '2026-05-12'}], 'testimonial_framing': {'template': 'Acme shipped in 2 weeks.', 'approved_by_customers': ['Acme']}, 'owner': '@ruslan'}
BAD = {'program_id': 'x', 'incentive': {'type': 'percent', 'amount_usd': 10}, 'attribution_window_days': 365, 'referrers': [{'handle': '@x'}], 'partners': [], 'testimonial_framing': {}, 'owner': 'team'}


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
