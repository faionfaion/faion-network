#!/usr/bin/env python3
"""validate-cross-channel-cpa-rollup.py

Validate one CPA rollup row JSON against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to rollup row JSON
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

WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
REQUIRED = (
    "week", "channel", "gross_spend_usd", "attributed_conversions",
    "self_reported_conversions", "view_through_count", "cpa_gross",
    "incremental_over_organic", "cpa_incremental",
    "cohort_d30_retention", "attribution_policy_version",
)


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required: {k}")
    if obj.get("week") and not WEEK_RE.match(obj["week"]):
        errs.append("week must match YYYY-Www")
    for nk in ("gross_spend_usd", "cpa_gross", "cpa_incremental"):
        v = obj.get(nk)
        if v is not None and (not isinstance(v, (int, float)) or v < 0):
            errs.append(f"{nk} must be non-negative number")
    if obj.get("attribution_policy_version") and not SEMVER.match(obj["attribution_policy_version"]):
        errs.append("attribution_policy_version must be semver")
    for rk in ("cohort_d30_retention", "cohort_d60_retention", "cohort_d90_retention"):
        v = obj.get(rk)
        if v is not None and not (isinstance(v, (int, float)) and 0 <= v <= 1):
            errs.append(f"{rk} must be in [0,1] or null")
    # rule single-attribution-model: view-through must not exceed attributed (sanity)
    a = obj.get("attributed_conversions")
    s = obj.get("self_reported_conversions")
    if isinstance(a, int) and isinstance(s, int) and a > s and s > 0:
        errs.append("attributed_conversions > self_reported_conversions (view-through likely added)")
    return errs


OK = {
    "week": "2026-W20", "channel": "Meta-paid", "gross_spend_usd": 4800.0,
    "attributed_conversions": 32, "self_reported_conversions": 51, "view_through_count": 18,
    "cpa_gross": 150.0, "incremental_over_organic": 22, "cpa_incremental": 218.18,
    "cohort_d30_retention": 0.71, "attribution_policy_version": "1.2.0",
}
BAD = {"week": "W20", "channel": "Meta"}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write(f"ok rejected: {validate(OK)}\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
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
        sys.stderr.write(f"not a file: {p}\n"); return 2
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
