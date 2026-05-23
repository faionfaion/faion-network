#!/usr/bin/env python3
"""validate-benefits-realization.py

Validate a spec artefact for Benefits Realization against the schema in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    path to artefact JSON
    --self-test    run built-in fixtures and exit
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['project_id', 'owner_of_register', 'benefits']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    benefits = obj.get("benefits") or []
    if not isinstance(benefits, list) or not benefits:
        errs.append("benefits must be non-empty list")
    else:
        for i, b in enumerate(benefits):
            for k in ("id", "metric", "baseline_value", "baseline_date",
                      "target_value", "target_date", "owner", "attribution_plan"):
                if k not in b:
                    errs.append(f"benefits[{i}].{k} missing")

    return errs


GOOD = {'project_id': 'acme-crm-2026', 'owner_of_register': 'U_VP_SALES', 'benefits': [{'id': 'b1', 'metric': 'deals_closed_per_q', 'baseline_value': 120, 'baseline_date': '2026-01-01', 'target_value': 144, 'target_date': '2026-12-31', 'owner': 'U_VP_SALES', 'attribution_plan': 'diff-in-diff'}]}
BAD = {'project_id': 'x', 'owner_of_register': '', 'benefits': [{'id': 'b1', 'metric': 'growth'}]}


def self_test():
    if validate(GOOD):
        sys.stderr.write("good rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n"); return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
