#!/usr/bin/env python3
"""validate-solo-time-tracking-discipline.py

Validate the TimeReport artefact against the JSON Schema in
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
WRITE_OFF_REASONS = {"SALES", "ADMIN", "LEARNING", "UNBILLABLE-REWORK", "BREAK"}
REQUIRED = [
    "week_iso",
    "billable_hours_by_project",
    "write_offs",
    "untagged_remaining",
    "billable_pct_actual",
    "gaps_detected",
    "invoice_drafts",
]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    wi = obj.get("week_iso")
    if isinstance(wi, str) and not WEEK_RE.match(wi):
        errs.append("week_iso must match YYYY-Wnn")
    ur = obj.get("untagged_remaining")
    if isinstance(ur, (int, float)) and ur > 1.0:
        errs.append("untagged_remaining must be <= 1.0")
    bp = obj.get("billable_pct_actual")
    if isinstance(bp, (int, float)) and bp > 0.65 and obj.get("data_warning") is not True:
        errs.append("billable_pct_actual > 0.65 requires data_warning=true")
    wos = obj.get("write_offs", [])
    if isinstance(wos, list):
        for i, w in enumerate(wos):
            if not isinstance(w, dict):
                continue
            if w.get("reason") not in WRITE_OFF_REASONS:
                errs.append(f"write_offs[{i}].reason not in closed list")
    inv = obj.get("invoice_drafts", [])
    if isinstance(inv, list):
        for i, d in enumerate(inv):
            lines = d.get("lines", []) if isinstance(d, dict) else []
            for j, ln in enumerate(lines):
                if not isinstance(ln, dict):
                    continue
                if ln.get("hours") == 0 or ln.get("rate") == 0:
                    errs.append(f"invoice_drafts[{i}].lines[{j}] has hours==0 or rate==0")
    if "gaps_detected" not in obj:
        errs.append("gaps_detected must be present (may be empty)")
    return errs


OK = {
    "week_iso": "2026-W21",
    "billable_hours_by_project": [
        {"project": "client-a", "hours": 14, "rate": 145, "amount": 2030},
        {"project": "client-b", "hours": 6, "rate": 145, "amount": 870},
    ],
    "write_offs": [
        {"reason": "SALES", "hours": 3},
        {"reason": "ADMIN", "hours": 2},
        {"reason": "LEARNING", "hours": 1.5},
        {"reason": "BREAK", "hours": 5},
    ],
    "untagged_remaining": 0.25,
    "billable_pct_actual": 0.541,
    "top_tasks": [{"task_label": "dev", "hours": 12}, {"task_label": "review", "hours": 4}],
    "gaps_detected": [],
    "invoice_drafts": [
        {"project": "client-a", "lines": [{"date": "2026-05-19", "task": "dev", "hours": 4, "rate": 145, "amount": 580}]}
    ],
}
BAD = {
    "week_iso": "2026W21",
    "billable_hours_by_project": [{"project": "client-a", "hours": 40, "rate": 145, "amount": 5800}],
    "write_offs": [{"reason": "OTHER", "hours": 5}],
    "untagged_remaining": 4.5,
    "billable_pct_actual": 0.82,
    "invoice_drafts": [],
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
