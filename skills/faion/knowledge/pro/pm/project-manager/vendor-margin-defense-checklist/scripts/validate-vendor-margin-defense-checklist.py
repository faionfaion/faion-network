#!/usr/bin/env python3
"""validate-vendor-margin-defense-checklist.py

Validate a MarginBleedReport against content/02-output-contract.xml. Stdlib-only.

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
import re
import sys
from pathlib import Path

WEEK_RX = re.compile(r"^[0-9]{4}-W[0-9]{2}$")
PATTERNS = {"silent_scope_creep", "free_analysis", "missing_change_request",
            "ai_rework_loop", "gold_plating", "sympathy_discount"}
TRIGGERS = {"single_pattern_gt_5pct", "cumulative_gt_10pct", "margin_negative"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("project_id", "week_iso", "baseline_margin_pct", "current_realised_margin_pct",
             "bleeds", "cumulative_bleed_pct", "alerts_triggered", "recommended_actions",
             "comms_drafted"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    if not WEEK_RX.match(obj["week_iso"]):
        errs.append("week_iso must match YYYY-Www")

    for i, b in enumerate(obj["bleeds"]):
        for k in ("pattern_id", "severity_pct_of_margin", "evidence", "hours_or_dollars", "first_detected_at"):
            if k not in b:
                errs.append(f"bleeds[{i}].{k} missing"); continue
        if b.get("pattern_id") not in PATTERNS:
            errs.append(f"bleeds[{i}].pattern_id invalid")
        if b.get("severity_pct_of_margin", 0) == 0 and b.get("hours_or_dollars", 0) > 0:
            errs.append(f"bleeds[{i}] severity=0 with hours>0 is inconsistent")

    max_single = max((b.get("severity_pct_of_margin", 0) for b in obj["bleeds"]), default=0)
    if max_single > 5 and not obj["alerts_triggered"]:
        errs.append("single bleed > 5% but no alert_triggered (rule: r3-bleed-alert-threshold)")
    if max_single > 5 and not obj["comms_drafted"]:
        errs.append("bleed > 5% but comms_drafted false (rule: r3-bleed-alert-threshold)")
    if obj["cumulative_bleed_pct"] > 10 and not obj["alerts_triggered"]:
        errs.append("cumulative > 10% but no alert_triggered")

    for i, a in enumerate(obj["alerts_triggered"]):
        for k in ("alert_id", "trigger", "pattern_id", "evidence", "recommended_conversation", "due_by"):
            if k not in a:
                errs.append(f"alerts_triggered[{i}].{k} missing")
        if a.get("trigger") not in TRIGGERS:
            errs.append(f"alerts_triggered[{i}].trigger invalid")
        if a.get("pattern_id") not in PATTERNS:
            errs.append(f"alerts_triggered[{i}].pattern_id invalid")
        if len(a.get("recommended_conversation", "")) < 40:
            errs.append(f"alerts_triggered[{i}].recommended_conversation too short")

    return errs


SMOKE_OK = {
    "project_id": "smoke", "week_iso": "2026-W21",
    "baseline_margin_pct": 30, "current_realised_margin_pct": 28,
    "bleeds": [], "cumulative_bleed_pct": 0, "alerts_triggered": [],
    "recommended_actions": [], "comms_drafted": False
}
SMOKE_BAD = {
    "project_id": "x", "week_iso": "2026-W21",
    "baseline_margin_pct": 30, "current_realised_margin_pct": 18,
    "bleeds": [{"pattern_id": "silent_scope_creep", "severity_pct_of_margin": 8,
                "evidence": ["msg"], "hours_or_dollars": 600,
                "first_detected_at": "2026-05-19"}],
    "cumulative_bleed_pct": 8, "alerts_triggered": [],
    "recommended_actions": [], "comms_drafted": False
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
