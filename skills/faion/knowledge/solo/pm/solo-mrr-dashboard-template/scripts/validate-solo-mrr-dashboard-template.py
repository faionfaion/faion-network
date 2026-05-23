#!/usr/bin/env python3
"""validate-solo-mrr-dashboard-template.py

Validate the monthly MRR dashboard artefact against the JSON Schema in
content/02-output-contract.xml.

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
import re
import sys
from pathlib import Path

MONTH_RE = re.compile(r"^[0-9]{4}-[0-9]{2}$")
REQUIRED = [
    "month",
    "mrr_usd",
    "gross_churn_pct",
    "arpu_usd",
    "ltv_usd",
    "customer_count",
    "annual_handling",
    "snapshot_frozen_on",
    "definitions",
]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if isinstance(obj.get("month"), str) and not MONTH_RE.match(obj["month"]):
        errs.append("month must match YYYY-MM")
    if obj.get("annual_handling") != "divide-by-12":
        errs.append("annual_handling must be 'divide-by-12'")
    if obj.get("refund_handling") not in (None, "subtract-in-month-only"):
        errs.append("refund_handling must be 'subtract-in-month-only'")
    g = obj.get("gross_churn_pct")
    if isinstance(g, (int, float)) and (g < 0 or g > 1):
        errs.append("gross_churn_pct must be 0..1")
    defs = obj.get("definitions")
    if isinstance(defs, dict):
        if defs.get("customer_definition") != "one-paid-subscription":
            errs.append("definitions.customer_definition must be 'one-paid-subscription'")
        if defs.get("churn_definition") not in ("gross", "net"):
            errs.append("definitions.churn_definition must be 'gross' or 'net'")
    elif "definitions" in obj:
        errs.append("definitions must be object")
    return errs


OK = {
    "month": "2026-04",
    "mrr_usd": 3210.00,
    "gross_churn_pct": 0.038,
    "net_churn_pct": 0.012,
    "arpu_usd": 29.10,
    "ltv_usd": 765.79,
    "customer_count": 110,
    "annual_handling": "divide-by-12",
    "refund_handling": "subtract-in-month-only",
    "snapshot_frozen_on": "2026-05-05",
    "definitions": {"customer_definition": "one-paid-subscription", "churn_definition": "gross"},
}
BAD = {
    "month": "April 2026",
    "mrr_usd": 12000,
    "gross_churn_pct": 1.5,
    "arpu_usd": 0,
    "ltv_usd": 0,
    "customer_count": 350,
    "annual_handling": "book-as-spike",
    "refund_handling": "retroactive-delete",
    "snapshot_frozen_on": "2026-05-05",
    "definitions": {"customer_definition": "auth-user", "churn_definition": "depends"},
}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
