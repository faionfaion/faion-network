#!/usr/bin/env python3
"""validate-team-morale-pulse-survey.py

Validate a MoralePulse aggregate JSON against the schema in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to MoralePulse JSON
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
TRIGGERS = {"enps_drop", "axis_median_low", "response_rate_low"}
ACTIONS = {"one_on_ones_within_48h", "survey_pause"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("team_id", "sprint_id", "week_iso", "responses_received", "team_size",
             "response_rate", "anonymity_threshold_met", "scores", "alerts_triggered"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    if not WEEK_RX.match(obj["week_iso"]):
        errs.append("week_iso must match YYYY-Www")
    if obj["team_size"] < 3:
        errs.append("team_size < 3 — methodology must be skipped (rule: r2-anonymity-floor)")
    rr = obj["response_rate"]
    if not (0 <= rr <= 1):
        errs.append("response_rate must be in [0,1]")

    threshold_met_expected = (obj["responses_received"] >= 3 and rr >= 0.6)
    if obj["anonymity_threshold_met"] != threshold_met_expected:
        errs.append("anonymity_threshold_met does not match (responses_received>=3 AND response_rate>=0.6)")

    scores = obj.get("scores", {})
    for axis in ("enps", "workload", "autonomy", "clarity"):
        if axis not in scores:
            errs.append(f"scores.{axis} missing")

    if not obj["anonymity_threshold_met"]:
        for axis in ("workload", "autonomy", "clarity"):
            s = scores.get(axis, {})
            if "median" in s and s["median"] not in (None, 0):
                errs.append(f"scores.{axis}.median populated while anonymity_threshold_met=false (rule: r2-anonymity-floor)")

    enps = scores.get("enps", {})
    if "value" in enps:
        v = enps["value"]
        if not isinstance(v, int) or not (-100 <= v <= 100):
            errs.append("scores.enps.value must be integer in [-100, 100] computed as %Promoters - %Detractors (rule: fm-06)")

    for i, a in enumerate(obj["alerts_triggered"]):
        for k in ("alert_id", "trigger", "evidence", "action_required", "due_by", "responsible_pm"):
            if k not in a:
                errs.append(f"alerts_triggered[{i}].{k} missing")
        if a.get("trigger") not in TRIGGERS:
            errs.append(f"alerts_triggered[{i}].trigger invalid")
        if a.get("action_required") not in ACTIONS:
            errs.append(f"alerts_triggered[{i}].action_required invalid")
    return errs


SMOKE_OK = {
    "team_id": "smoke", "sprint_id": "S14", "week_iso": "2026-W21",
    "responses_received": 5, "team_size": 6, "response_rate": 0.83,
    "anonymity_threshold_met": True,
    "scores": {"enps": {"value": -10}, "workload": {"mean": 6.5, "median": 7},
               "autonomy": {"mean": 7, "median": 7}, "clarity": {"mean": 7.5, "median": 8}},
    "alerts_triggered": []
}
SMOKE_BAD = {
    "team_id": "x", "sprint_id": "S14", "week_iso": "2026-W21",
    "responses_received": 1, "team_size": 2, "response_rate": 0.5,
    "anonymity_threshold_met": False,
    "scores": {"enps": {"value": 4.5}, "workload": {"mean": 4, "median": 4},
               "autonomy": {"mean": 5, "median": 5}, "clarity": {"mean": 6, "median": 6}},
    "alerts_triggered": []
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
