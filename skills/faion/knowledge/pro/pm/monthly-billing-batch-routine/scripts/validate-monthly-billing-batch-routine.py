#!/usr/bin/env python3
"""validate-monthly-billing-batch-routine.py — F-066 B4 stdlib validator for the Monthly Billing Batch Routine artefact.

Validates that an input JSON file satisfies the required-keys subset of the
schema declared in content/02-output-contract.xml of this methodology.

Inputs:
    --file PATH       path to artefact JSON file
    --self-test       run built-in pass/fail fixtures
    --help            show this message

Exit codes:
    0 — valid
    1 — invalid (violations printed to stderr)
    2 — usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['batch_id', 'month', 'customer_invoices', 'contractor_payouts', 'margin', 'prior_month_delta', 'status']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
        elif obj[k] is None:
            errs.append(f"required field is null: {k}")
    return errs


OK_FIXTURE = json.loads('{"batch_id": "mbbr-2026-05", "month": "2026-05", "customer_invoices": [{"customer_id": "acme", "amount": 12000, "currency": "EUR", "evidence": [{"source": "SoW-acme-2026", "citation": "monthly retainer 12000"}]}], "contractor_payouts": [{"contractor_id": "olena-k", "amount": 6400, "currency": "EUR", "evidence": [{"source": "timesheet-2026-05.csv", "citation": "40h @ 160"}]}], "margin": {"computed": true, "invoices_total": 12000, "payouts_total": 6400}, "prior_month_delta": {"outstanding_invoices": [], "unpaid_payouts": []}, "status": "ready_for_review"}')
BAD_FIXTURE = json.loads('{"batch_id": "mbbr", "month": "2026", "customer_invoices": [], "status": "approved_to_send"}')


def self_test() -> int:
    errs = validate(OK_FIXTURE)
    if errs:
        sys.stderr.write("self-test: valid fixture rejected — " + "; ".join(errs) + "\n")
        return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("self-test: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"json parse error: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
