#!/usr/bin/env python3
"""validate-qa-risk-matrix-method.py

Validate the risk-matrix + investment-plan artefact against the JSON Schema
in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

QUADRANTS = {"HH", "HL", "LH", "LL"}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in ("matrix", "investment_plan"):
        if k not in obj:
            errs.append(f"missing required top-level field: {k}")
    matrix = obj.get("matrix")
    quadrants_present = set()
    if isinstance(matrix, dict):
        if "refreshed_at" not in matrix:
            errs.append("matrix.refreshed_at missing")
        areas = matrix.get("areas")
        if not isinstance(areas, list) or len(areas) < 5 or len(areas) > 25:
            errs.append("matrix.areas must be an array with 5..25 entries")
        else:
            impact_counts = [0] * 6
            for i, a in enumerate(areas):
                if not isinstance(a, dict):
                    errs.append(f"matrix.areas[{i}] not an object")
                    continue
                for k in ("name", "impact", "impact_rationale", "likelihood", "likelihood_data", "adjustment_pm1", "quadrant"):
                    if k not in a:
                        errs.append(f"matrix.areas[{i}].{k} missing")
                imp = a.get("impact")
                if isinstance(imp, int):
                    if imp < 1 or imp > 5:
                        errs.append(f"matrix.areas[{i}].impact must be 1..5")
                    else:
                        impact_counts[imp] += 1
                rationale = a.get("impact_rationale", "")
                if isinstance(rationale, str) and len(rationale) < 15:
                    errs.append(f"matrix.areas[{i}].impact_rationale must be at least 15 characters")
                lik = a.get("likelihood")
                if isinstance(lik, int) and (lik < 1 or lik > 5):
                    errs.append(f"matrix.areas[{i}].likelihood must be 1..5")
                ld = a.get("likelihood_data")
                if not isinstance(ld, dict):
                    errs.append(f"matrix.areas[{i}].likelihood_data must be object")
                else:
                    for lk in ("incidents_6m", "commits_6m"):
                        if lk not in ld:
                            errs.append(f"matrix.areas[{i}].likelihood_data.{lk} missing")
                adj = a.get("adjustment_pm1")
                if isinstance(adj, int) and (adj < -1 or adj > 1):
                    errs.append(f"matrix.areas[{i}].adjustment_pm1 must be -1..1")
                q = a.get("quadrant")
                if q and q not in QUADRANTS:
                    errs.append(f"matrix.areas[{i}].quadrant must be one of {sorted(QUADRANTS)}")
                if q in QUADRANTS:
                    quadrants_present.add(q)
            high_count = impact_counts[4] + impact_counts[5]
            if isinstance(areas, list) and len(areas) >= 5 and high_count == len(areas):
                errs.append("flat-impact distribution: every area scored 4 or 5")
    inv = obj.get("investment_plan")
    if isinstance(inv, dict):
        for q in ("HH", "HL", "LH", "LL", "capacity_check"):
            if q not in inv:
                errs.append(f"investment_plan.{q} missing")
        for q in ("HH", "HL", "LH", "LL"):
            v = inv.get(q, "")
            if q in quadrants_present and isinstance(v, str) and len(v.strip()) < 20:
                errs.append(f"investment_plan.{q} entry too short (<20 chars) while areas exist in quadrant {q}")
        cap = inv.get("capacity_check")
        if isinstance(cap, dict):
            for k in ("required_hours", "team_capacity_hours"):
                if k not in cap:
                    errs.append(f"investment_plan.capacity_check.{k} missing")
            rh = cap.get("required_hours")
            tc = cap.get("team_capacity_hours")
            if isinstance(rh, (int, float)) and isinstance(tc, (int, float)) and tc > 0:
                if rh > 1.5 * tc:
                    errs.append("capacity overrun: required_hours > 1.5x team_capacity_hours (plan is unrealistic)")
    return errs


def self_test() -> int:
    good = {
        "matrix": {
            "refreshed_at": "2026-05-23",
            "areas": [
                {"name": "billing-subscription-lifecycle", "impact": 5, "impact_rationale": "revenue loss within hours; dispute support cost", "likelihood": 4, "likelihood_data": {"incidents_6m": 2, "commits_6m": 120}, "adjustment_pm1": 0, "quadrant": "HH"},
                {"name": "search-and-filtering", "impact": 3, "impact_rationale": "degraded search slows users but no money loss", "likelihood": 4, "likelihood_data": {"incidents_6m": 5, "commits_6m": 80}, "adjustment_pm1": 0, "quadrant": "LH"},
                {"name": "tenant-isolation", "impact": 5, "impact_rationale": "data residency breach is a regulatory fine", "likelihood": 1, "likelihood_data": {"incidents_6m": 0, "commits_6m": 5}, "adjustment_pm1": 0, "quadrant": "HL"},
                {"name": "admin-audit-log", "impact": 1, "impact_rationale": "internal convenience; never customer-visible", "likelihood": 1, "likelihood_data": {"incidents_6m": 0, "commits_6m": 2}, "adjustment_pm1": 0, "quadrant": "LL"},
                {"name": "auth-login-and-signup", "impact": 5, "impact_rationale": "lock-out blocks every customer", "likelihood": 3, "likelihood_data": {"incidents_6m": 1, "commits_6m": 40}, "adjustment_pm1": 0, "quadrant": "HH"},
            ],
        },
        "investment_plan": {
            "HH": "mandatory unit + integration + e2e + monthly exploratory; owned by Ruslan",
            "HL": "mandatory unit + integration + targeted exploratory; owned by Anna",
            "LH": "automation only (unit + light integration); owned by Bohdan",
            "LL": "monitor-only; no investment until risk shifts",
            "capacity_check": {"required_hours": 32, "team_capacity_hours": 40},
        },
    }
    errs = validate(good)
    if errs:
        sys.stderr.write("self-test: good fixture rejected: " + json.dumps(errs) + "\n")
        return 1
    bad = {
        "matrix": {
            "refreshed_at": "2024-01-01",
            "areas": [{"name": "all", "impact": 5, "impact_rationale": "high", "likelihood": 5, "quadrant": "HH", "adjustment_pm1": 0}],
        },
        "investment_plan": {"HH": "x", "HL": "x", "LH": "x", "LL": "x", "capacity_check": {"required_hours": 200, "team_capacity_hours": 40}},
    }
    if not validate(bad):
        sys.stderr.write("self-test: bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
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
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
