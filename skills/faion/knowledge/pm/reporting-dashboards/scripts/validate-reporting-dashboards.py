#!/usr/bin/env python3
"""validate-reporting-dashboards.py

Validate the report artefact for the reporting-dashboards methodology against
the JSON Schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to report artefact JSON
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

STATUS_ENUM = {"On Track", "At Risk", "Off Track"}
REQUIRED = [
    "sprint_id",
    "status",
    "metrics",
    "thresholds",
    "archive_url",
    "fetch_errors",
    "validated",
    "delivered_to",
]
REQUIRED_METRICS = ["committed", "completed", "completion_rate", "scope_creep", "blocked_count"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if obj.get("status") not in STATUS_ENUM:
        errs.append("status must be one of " + ", ".join(sorted(STATUS_ENUM)))
    metrics = obj.get("metrics")
    if isinstance(metrics, dict):
        for k in REQUIRED_METRICS:
            if k not in metrics:
                errs.append("metrics missing: " + k)
        committed = metrics.get("committed")
        if committed is not None and (not isinstance(committed, int) or committed < 1):
            errs.append("metrics.committed must be int >= 1 (0 signals silent fetch failure)")
        cr = metrics.get("completion_rate")
        if cr is not None and (not isinstance(cr, (int, float)) or cr < 0 or cr > 1):
            errs.append("metrics.completion_rate must be 0..1")
    elif "metrics" in obj:
        errs.append("metrics must be object")
    fe = obj.get("fetch_errors")
    if fe is not None and fe != 0:
        errs.append("fetch_errors must be 0 (else do not deliver)")
    if obj.get("validated") is not True:
        errs.append("validated must be true to deliver")
    if not obj.get("archive_url"):
        errs.append("archive_url must be present")
    dt = obj.get("delivered_to")
    if dt is not None and (not isinstance(dt, list) or len(dt) < 1):
        errs.append("delivered_to must be non-empty list")
    return errs


OK = {
    "sprint_id": "S-2026-W21",
    "status": "On Track",
    "metrics": {
        "committed": 24,
        "completed": 22,
        "completion_rate": 0.917,
        "scope_creep": 2,
        "blocked_count": 0,
    },
    "thresholds": {"on_track_min": 0.85, "at_risk_min": 0.70},
    "archive_url": "s3://reports/sprint-2026-w21.md",
    "dashboard_url": "https://metabase.example.com/dashboard/42",
    "fetch_errors": 0,
    "validated": True,
    "delivered_to": ["#leadership"],
    "generated_at": "2026-05-23T09:00:00Z",
}
BAD = {
    "sprint_id": "S-2026-W21",
    "status": "Healthy",
    "metrics": {"committed": 0, "completed": 0, "completion_rate": 0},
    "fetch_errors": 3,
    "validated": False,
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
