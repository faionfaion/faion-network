#!/usr/bin/env python3
"""validate-cost-estimation.py

Validate a spec artefact for Cost Estimation against the schema in
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

REQUIRED = ['project_id', 'wbs_leaves', 'contingency', 'management_reserve', 'total_mean', 'total_pessimistic']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    leaves = obj.get("wbs_leaves") or []
    if not isinstance(leaves, list) or not leaves:
        errs.append("wbs_leaves must be non-empty list")
    else:
        for i, lf in enumerate(leaves):
            for k in ("id", "name", "optimistic_hours", "most_likely_hours",
                      "pessimistic_hours", "pert_mean_hours", "rate_per_hour",
                      "historical_reference"):
                if k not in lf:
                    errs.append(f"wbs_leaves[{i}].{k} missing")
            o = lf.get("optimistic_hours"); m = lf.get("most_likely_hours")
            p = lf.get("pessimistic_hours"); pm = lf.get("pert_mean_hours")
            if all(isinstance(x, (int, float)) for x in (o, m, p, pm)):
                expected = (o + 4 * m + p) / 6
                if abs(pm - expected) > 0.5:
                    errs.append(f"wbs_leaves[{i}].pert_mean_hours mismatch (expected ~{expected:.2f})")
    for j, c in enumerate(obj.get("contingency") or []):
        if "risk_id" not in c:
            errs.append(f"contingency[{j}].risk_id missing")

    return errs


GOOD = {'project_id': 'acme', 'wbs_leaves': [{'id': 'wbs-1', 'name': 'x', 'optimistic_hours': 4, 'most_likely_hours': 8, 'pessimistic_hours': 16, 'pert_mean_hours': 8.67, 'rate_per_hour': 120, 'historical_reference': 'past-engagement-1'}], 'contingency': [{'risk_id': 'R-01', 'amount': 1000, 'rationale': 'x'}], 'management_reserve': 1500, 'total_mean': 1000, 'total_pessimistic': 2000}
BAD = {'project_id': 'x', 'wbs_leaves': [], 'contingency': [], 'management_reserve': 0, 'total_mean': 0, 'total_pessimistic': 0}


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
