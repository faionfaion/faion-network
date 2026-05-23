#!/usr/bin/env python3
"""validate-pricing-experiment-runbook.py

Validate the {plan, stripe_preflight, decision_memo} bundle against
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

AUDIENCE_ENUM = {"new_signups_only", "new_and_existing_with_grandfather", "specific_segment"}
SIG_ENUM = {"p<0.05", "p<0.10", "bayesian_95"}
TAX_ENUM = {"inclusive", "exclusive"}
DECISION_ENUM = {"adopt_new", "revert_to_old", "extend_with_adjustment"}


def _check_plan(plan, errs):
    req = ["experiment_id", "start_date", "end_date", "duration_days",
           "variant_old", "variant_new", "audience", "exposure_rule",
           "success_metric_primary", "success_metric_threshold",
           "significance_target", "guardrail_metrics", "grandfathering",
           "currencies_in_test", "tax_behavior"]
    for k in req:
        if k not in plan:
            errs.append("plan missing " + k)
    if "duration_days" in plan and (not isinstance(plan["duration_days"], int)
                                    or plan["duration_days"] < 7
                                    or plan["duration_days"] > 90):
        errs.append("plan.duration_days must be int in [7,90]")
    if "audience" in plan and plan["audience"] not in AUDIENCE_ENUM:
        errs.append("plan.audience not in enum")
    if "significance_target" in plan and plan["significance_target"] not in SIG_ENUM:
        errs.append("plan.significance_target not in enum")
    if "tax_behavior" in plan and plan["tax_behavior"] not in TAX_ENUM:
        errs.append("plan.tax_behavior not in enum")
    if "variant_old" in plan and "stripe_price_id" not in plan.get("variant_old", {}):
        errs.append("plan.variant_old.stripe_price_id missing")
    if "variant_new" in plan and "stripe_price_id" not in plan.get("variant_new", {}):
        errs.append("plan.variant_new.stripe_price_id missing")
    if "grandfathering" in plan:
        gf = plan["grandfathering"]
        for k in ("audience", "mechanism", "stripe_coupon_id", "window_months"):
            if k not in gf:
                errs.append("plan.grandfathering missing " + k)
    if "currencies_in_test" in plan:
        cit = plan["currencies_in_test"]
        if not isinstance(cit, list) or len(cit) < 1:
            errs.append("plan.currencies_in_test must be non-empty list")
    if "guardrail_metrics" in plan:
        gm = plan["guardrail_metrics"]
        if not isinstance(gm, list) or len(gm) < 1:
            errs.append("plan.guardrail_metrics must be non-empty list")


def _check_preflight(pf, errs):
    for k in ("passed_at", "checks_run"):
        if k not in pf:
            errs.append("stripe_preflight missing " + k)
    if "checks_run" in pf:
        cr = pf["checks_run"]
        if not isinstance(cr, list) or len(cr) < 4:
            errs.append("stripe_preflight.checks_run must have >=4 entries")


def _check_memo(memo, errs):
    for k in ("written_at", "decision", "metric_readouts", "next_action"):
        if k not in memo:
            errs.append("decision_memo missing " + k)
    if "decision" in memo and memo["decision"] not in DECISION_ENUM:
        errs.append("decision_memo.decision not in enum")
    if "next_action" in memo and (not isinstance(memo["next_action"], str)
                                  or len(memo["next_action"]) < 5):
        errs.append("decision_memo.next_action too short")


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("plan", "stripe_preflight", "decision_memo"):
        if k not in obj:
            errs.append("missing required top-level: " + k)
    if "plan" in obj and isinstance(obj["plan"], dict):
        _check_plan(obj["plan"], errs)
    if "stripe_preflight" in obj and isinstance(obj["stripe_preflight"], dict):
        _check_preflight(obj["stripe_preflight"], errs)
    if "decision_memo" in obj and isinstance(obj["decision_memo"], dict):
        _check_memo(obj["decision_memo"], errs)
    return errs


OK = {
    "plan": {
        "experiment_id": "exp-smoke",
        "start_date": "2026-06-01",
        "end_date": "2026-07-30",
        "duration_days": 60,
        "variant_old": {"stripe_price_id": "price_old"},
        "variant_new": {"stripe_price_id": "price_new"},
        "audience": "new_signups_only",
        "exposure_rule": "random 50/50 by signup-id hash",
        "success_metric_primary": "trial_to_paid_conversion_pct",
        "success_metric_threshold": 0.18,
        "significance_target": "p<0.05",
        "guardrail_metrics": ["refund_rate", "dispute_rate"],
        "grandfathering": {
            "audience": "all subs before start",
            "mechanism": "100% off coupon",
            "stripe_coupon_id": "grandfather_smoke",
            "window_months": 12,
        },
        "currencies_in_test": ["usd"],
        "tax_behavior": "exclusive",
    },
    "stripe_preflight": {
        "passed_at": "2026-05-28T09:00:00Z",
        "checks_run": ["new_price_exists", "old_price_active", "coupon_attached", "no_orphan_subs"],
    },
    "decision_memo": {
        "written_at": "2026-07-31T18:00:00Z",
        "decision": "adopt_new",
        "metric_readouts": {"new": 0.21, "old": 0.17},
        "qualitative_signals": "no spike",
        "next_action": "Move all signups to price_new on 2026-08-01.",
    },
}
BAD = {"plan": {"experiment_id": "x", "duration_days": 200},
       "stripe_preflight": {"checks_run": []},
       "decision_memo": {}}


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
