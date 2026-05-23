#!/usr/bin/env python3
"""validate-value-stream-management.py

Validate a ValueStreamReport JSON against the schema in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to report JSON
    --self-test       run built-in fixtures
    --help            this message

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

WORK_TYPES = ("feature", "defect", "risk", "debt")
TIER_LABELS = {"low", "medium", "high", "elite"}
FLOW_FIELDS = ("lead_time_days", "cycle_time_days", "throughput_per_week",
               "wip", "complete_and_accurate_pct", "sample_size")
INTERNAL_ANCHORS = {"ticket created", "issue opened", "ticket_created", "issue_opened"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("stream_id", "window", "customer_anchor", "flow_metrics_by_type",
             "dora", "constraint", "experiments"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    if obj["window"].get("days", 0) < 30:
        errs.append("window.days must be >= 30")

    ca = obj["customer_anchor"]
    if ca.get("start_event", "").lower() in INTERNAL_ANCHORS or ca.get("end_event", "").lower() == "merged":
        errs.append("customer_anchor uses internal endpoints (rule: customer-anchored-boundary)")

    fmt = obj["flow_metrics_by_type"]
    missing = [w for w in WORK_TYPES if w not in fmt]
    if missing:
        errs.append(f"flow_metrics_by_type missing work types: {missing} (rule: work-type-split)")
    for w in WORK_TYPES:
        if w not in fmt:
            continue
        for f in FLOW_FIELDS:
            if f not in fmt[w]:
                errs.append(f"flow_metrics_by_type.{w}.{f} missing")

    dora = obj["dora"]
    df = dora.get("deployment_frequency")
    if not isinstance(df, dict) or "human_prs" not in df or "bot_prs" not in df:
        errs.append("dora.deployment_frequency must be {human_prs, bot_prs} (rule: ai-pr-bot-split)")
    if dora.get("tier_label") is not None:
        if dora["tier_label"] not in TIER_LABELS:
            errs.append("dora.tier_label invalid")
        if dora.get("trend_window_quarters", 0) < 2:
            errs.append("dora.tier_label present but trend_window_quarters < 2 (rule: no-elite-label-without-trend)")

    constraint = obj["constraint"]
    if constraint.get("stage"):
        spt = constraint.get("samples_per_type", {})
        too_small = [w for w in WORK_TYPES if spt.get(w, 0) < 50]
        if too_small:
            errs.append(f"constraint declared but samples < 50 for: {too_small} (rule: fifty-item-minimum-before-constraint)")
        if len(constraint.get("evidence", "")) < 20:
            errs.append("constraint.evidence must be >= 20 chars")

    if not isinstance(obj["experiments"], list) or not (1 <= len(obj["experiments"]) <= 3):
        errs.append("experiments must be a 1-3 item list")
    return errs


SMOKE_OK = {
    "stream_id": "smoke", "window": {"start": "2026-02-22", "end": "2026-05-23", "days": 90},
    "customer_anchor": {"start_event": "support_ticket_opened", "end_event": "feature_visible_in_prod"},
    "flow_metrics_by_type": {
        w: {"lead_time_days": 10, "cycle_time_days": 2, "throughput_per_week": 5,
            "wip": 4, "complete_and_accurate_pct": 0.9, "sample_size": 60}
        for w in WORK_TYPES
    },
    "dora": {"deployment_frequency": {"human_prs": 100, "bot_prs": 20},
             "change_lead_time_minutes": 90, "change_failure_rate": 0.05,
             "mttr_minutes": 30, "trend_window_quarters": 3, "tier_label": "high"},
    "constraint": {"stage": "design-review", "evidence": "long-enough evidence string",
                   "samples_per_type": {w: 60 for w in WORK_TYPES}},
    "experiments": [{"name": "WIP cap", "expected_lift": "-25%", "cost": "low", "rank": 1}]
}
SMOKE_BAD = {
    "stream_id": "x", "window": {"start": "2026-04-22", "end": "2026-05-23", "days": 31},
    "customer_anchor": {"start_event": "ticket created", "end_event": "merged"},
    "flow_metrics_by_type": {"feature": {"lead_time_days": 12, "cycle_time_days": 4,
        "throughput_per_week": 5, "wip": 10, "complete_and_accurate_pct": 0.7, "sample_size": 18}},
    "dora": {"deployment_frequency": 47, "change_lead_time_minutes": 60,
             "change_failure_rate": 0.05, "mttr_minutes": 20,
             "trend_window_quarters": 1, "tier_label": "elite"},
    "constraint": {"stage": "design-review", "evidence": "vibes",
                   "samples_per_type": {"feature": 18}},
    "experiments": []
}


def self_test() -> int:
    if validate(SMOKE_OK):
        sys.stderr.write("smoke_ok rejected: " + "; ".join(validate(SMOKE_OK)) + "\n"); return 1
    if not validate(SMOKE_BAD):
        sys.stderr.write("smoke_bad accepted\n"); return 1
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
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
