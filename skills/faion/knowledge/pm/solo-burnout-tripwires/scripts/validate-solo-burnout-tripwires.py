#!/usr/bin/env python3
"""validate-solo-burnout-tripwires.py

Validate the weekly tripwire-review artefact against the JSON Schema in
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

WEEK_RE = re.compile(r"^[0-9]{4}-W[0-9]{2}$")
VERDICTS = {"green", "amber", "red"}
ACTIONS = {
    "continue",
    "schedule-recovery",
    "block-feature-work",
    "review-pricing-or-audience",
    "schedule-non-product-activity",
    "book-health-appointment",
    "schedule-conversation",
}
REQUIRED = [
    "week_iso",
    "sleep_7d_mean_minutes",
    "weekend_days_in_4w_window",
    "mrr_to_hours_3m_slope",
    "joy_channel_logged",
    "deferred_health_count_12m",
    "non_transactional_contacts_w",
    "verdict",
    "action",
]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if isinstance(obj.get("week_iso"), str) and not WEEK_RE.match(obj["week_iso"]):
        errs.append("week_iso must match YYYY-Wnn")
    if obj.get("verdict") not in VERDICTS:
        errs.append("verdict must be in {green, amber, red}")
    if obj.get("action") not in ACTIONS:
        errs.append("action must be in closed enum")
    if not isinstance(obj.get("joy_channel_logged"), list):
        errs.append("joy_channel_logged must be array")
    s = obj.get("sleep_7d_mean_minutes")
    if isinstance(s, int) and s < 390 and obj.get("verdict") == "green":
        errs.append("sleep < 6h30m must not be reported green")
    return errs


OK = {
    "week_iso": "2026-W21",
    "sleep_7d_mean_minutes": 412,
    "weekend_days_in_4w_window": 1,
    "mrr_to_hours_3m_slope": 0.04,
    "joy_channel_logged": ["climbing-gym-tue", "dinner-w-mira-sat"],
    "deferred_health_count_12m": 1,
    "non_transactional_contacts_w": 2,
    "verdict": "green",
    "action": "continue",
}
BAD = {
    "week_iso": "this week",
    "sleep_7d_mean_minutes": 360,
    "weekend_days_in_4w_window": 4,
    "mrr_to_hours_3m_slope": -0.02,
    "joy_channel_logged": [],
    "deferred_health_count_12m": 4,
    "non_transactional_contacts_w": 0,
    "verdict": "fine",
    "action": "push through",
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
