#!/usr/bin/env python3
"""validate-solo-rate-floor-calculator.py

Validate the RateFloor artefact against the JSON Schema in
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
import sys
from pathlib import Path

REQUIRED = ["floor_usd_per_hour", "sensitivity", "project_minimum_usd", "breakdown", "defense_narrative", "computed_at"]
BREAKDOWN_REQUIRED = ["target_income_loaded", "tax_load_pct", "working_weeks", "billable_pct", "benefit_cost_usd", "tooling_cost_usd", "profit_margin_pct"]
LEAK_TOKENS = ["salary", "my income", "my mortgage", "my expenses", "my taxes"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    sens = obj.get("sensitivity")
    if isinstance(sens, list):
        if len(sens) != 3:
            errs.append("sensitivity must have exactly 3 bands")
        bands_seen = set()
        for i, s in enumerate(sens):
            if not isinstance(s, dict):
                errs.append(f"sensitivity[{i}] not object")
                continue
            bands_seen.add(s.get("band"))
        for b in ("low", "baseline", "high"):
            if b not in bands_seen:
                errs.append("sensitivity missing band: " + b)
    elif "sensitivity" in obj:
        errs.append("sensitivity must be array")
    bd = obj.get("breakdown")
    if isinstance(bd, dict):
        for k in BREAKDOWN_REQUIRED:
            if k not in bd:
                errs.append("breakdown missing: " + k)
        if bd.get("working_weeks", 0) > 46:
            errs.append("breakdown.working_weeks must be <= 46")
        bp = bd.get("billable_pct")
        if isinstance(bp, (int, float)) and bp > 0.55:
            if not obj.get("inputs_warning"):
                errs.append("billable_pct > 0.55 requires inputs_warning with historical-data source")
        pm = bd.get("profit_margin_pct")
        if isinstance(pm, (int, float)) and pm < 0.15:
            errs.append("breakdown.profit_margin_pct must be >= 0.15")
    elif "breakdown" in obj:
        errs.append("breakdown must be object")
    dn = obj.get("defense_narrative", "")
    if isinstance(dn, str):
        if len(dn) > 400:
            errs.append("defense_narrative must be <= 400 chars")
        low = dn.lower()
        for t in LEAK_TOKENS:
            if t in low:
                errs.append("defense_narrative leaks personal info: contains '" + t + "'")
                break
    return errs


OK = {
    "floor_usd_per_hour": 145,
    "sensitivity": [
        {"band": "low", "billable_pct": 0.45, "floor_usd_per_hour": 178},
        {"band": "baseline", "billable_pct": 0.55, "floor_usd_per_hour": 145},
        {"band": "high", "billable_pct": 0.65, "floor_usd_per_hour": 123},
    ],
    "project_minimum_usd": 2900,
    "breakdown": {
        "target_income_loaded": 144000,
        "tax_load_pct": 0.34,
        "working_weeks": 46,
        "billable_pct": 0.55,
        "benefit_cost_usd": 8000,
        "tooling_cost_usd": 3000,
        "profit_margin_pct": 0.20,
    },
    "defense_narrative": "Loaded rate accounting for downtime, taxes, tooling, and a 20% reinvestment margin standard for senior independent practice.",
    "inputs_warning": [],
    "computed_at": "2026-05-23",
}
BAD = {
    "floor_usd_per_hour": 58,
    "sensitivity": [],
    "project_minimum_usd": 100,
    "breakdown": {
        "target_income_loaded": 120000,
        "tax_load_pct": 0.10,
        "working_weeks": 52,
        "billable_pct": 0.80,
        "benefit_cost_usd": 0,
        "tooling_cost_usd": 0,
        "profit_margin_pct": 0.05,
    },
    "defense_narrative": "I need $120k salary to cover my mortgage and family expenses.",
    "computed_at": "2026-05-23",
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
