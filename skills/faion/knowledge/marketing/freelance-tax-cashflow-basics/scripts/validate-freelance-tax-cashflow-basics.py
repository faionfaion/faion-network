#!/usr/bin/env python3
"""validate-freelance-tax-cashflow-basics.py — schema validator. --self-test runs built-in fixtures."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
REQUIRED = ['checklist_id', 'checks', 'computed_at', 'owner']


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
    ck = obj.get("checks") or {}
    if ck.get("separate_account") is False:
        errs.append("separate_account=false (rule separate-business-account)")
    vat = ck.get("vat_reverse_charge") or {}
    if vat.get("b2b_eu_invoices_count", 0) > 0 and vat.get("all_carry_notation") is False:
        errs.append("EU B2B invoice missing reverse-charge notation (rule eu-reverse-charge-b2b)")
    et = ck.get("entity_threshold") or {}
    if et.get("annual_revenue_usd", 0) > 50000 and et.get("entity") == "sole_trader":
        errs.append("revenue >50k as sole_trader (rule entity-threshold-decision)")
    rm = ck.get("runway_months")
    if isinstance(rm, (int, float)) and rm < 6:
        errs.append("runway_months <6 (rule six-month-personal-runway)")

    return errs


OK = {'checklist_id': 'ftc-x', 'checks': {'estimated_tax': {'quarter': '2026-Q2', 'paid': True, 'amount_usd': 4200}, 'vat_reverse_charge': {'b2b_eu_invoices_count': 3, 'all_carry_notation': True}, 'entity_threshold': {'annual_revenue_usd': 62000, 'entity': 'llc'}, 'separate_account': True, 'runway_months': 7.5}, 'computed_at': '2026-05-23', 'owner': '@ruslan'}
BAD = {'checklist_id': 'x', 'checks': {'separate_account': False, 'estimated_tax': {'quarter': 'Q2', 'paid': False, 'amount_usd': 0}, 'vat_reverse_charge': {'b2b_eu_invoices_count': 0, 'all_carry_notation': False}, 'entity_threshold': {'annual_revenue_usd': 80000, 'entity': 'sole_trader'}, 'runway_months': 1}, 'owner': 'team', 'computed_at': '2026-05-23'}


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
