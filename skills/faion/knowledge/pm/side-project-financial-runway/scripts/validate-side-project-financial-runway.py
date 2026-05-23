#!/usr/bin/env python3
"""validate-side-project-financial-runway.py

Validate the runway-model artefact against the JSON Schema in
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

QUARTER_RE = re.compile(r"^[0-9]{4}-Q[1-4]$")
REQUIRED = [
    "burn_personal",
    "burn_business",
    "savings_buffer",
    "mrr_current",
    "mrr_3mo_growth_pct",
    "leave_job_trigger",
    "geo_arbitrage_scenario",
    "stress_tests",
    "review_quarter",
    "owner",
]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    rq = obj.get("review_quarter")
    if isinstance(rq, str) and not QUARTER_RE.match(rq):
        errs.append("review_quarter must match YYYY-Qn")
    if not obj.get("owner"):
        errs.append("owner must be non-empty")
    trig = obj.get("leave_job_trigger")
    if isinstance(trig, dict):
        if trig.get("runway_months", 0) < 12:
            errs.append("leave_job_trigger.runway_months must be >= 12")
        if trig.get("mrr_pct_of_burn", 0) < 0.30:
            errs.append("leave_job_trigger.mrr_pct_of_burn must be >= 0.30")
        if trig.get("growth_min", -1) < 0:
            errs.append("leave_job_trigger.growth_min must be >= 0")
    geo = obj.get("geo_arbitrage_scenario")
    if isinstance(geo, dict):
        if not geo.get("target_city"):
            errs.append("geo_arbitrage_scenario.target_city must be non-empty")
        if geo.get("expected_burn_reduction_pct") is None:
            errs.append("geo_arbitrage_scenario.expected_burn_reduction_pct missing")
    elif "geo_arbitrage_scenario" in obj:
        errs.append("geo_arbitrage_scenario must be object")
    st = obj.get("stress_tests")
    if isinstance(st, list):
        if len(st) < 2:
            errs.append("stress_tests must have >= 2 scenarios")
        for i, s in enumerate(st):
            if not isinstance(s, dict) or "scenario" not in s or "runway_at_that_burn" not in s:
                errs.append(f"stress_tests[{i}] missing scenario/runway_at_that_burn")
    return errs


OK = {
    "burn_personal": 6000,
    "burn_business": 1000,
    "savings_buffer": 90000,
    "mrr_current": 2500,
    "mrr_3mo_growth_pct": 0.12,
    "leave_job_trigger": {"runway_months": 12, "mrr_pct_of_burn": 0.36, "growth_min": 0},
    "geo_arbitrage_scenario": {"target_city": "Lisbon", "expected_burn_reduction_pct": 0.45},
    "stress_tests": [
        {"scenario": "flat MRR 12mo", "runway_at_that_burn": 12.8},
        {"scenario": "MRR -20% over 6mo", "runway_at_that_burn": 11.2},
    ],
    "review_quarter": "2026-Q2",
    "owner": "Ruslan",
    "decision_status": "stay-and-prepare",
}
BAD = {
    "burn_personal": 2000,
    "burn_business": 100,
    "savings_buffer": 12000,
    "mrr_current": 500,
    "mrr_3mo_growth_pct": -0.05,
    "leave_job_trigger": {"runway_months": 6, "mrr_pct_of_burn": 0.20, "growth_min": -0.05},
    "geo_arbitrage_scenario": {},
    "stress_tests": [],
    "review_quarter": "next quarter",
    "owner": "",
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
