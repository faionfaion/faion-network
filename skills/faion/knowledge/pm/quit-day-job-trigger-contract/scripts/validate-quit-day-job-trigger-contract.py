#!/usr/bin/env python3
"""validate-quit-day-job-trigger-contract.py

Validate the contract artefact against the JSON Schema in
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

KINDS = {"threshold", "event", "schedule"}
CADENCES = {"monthly", "quarterly"}
TEAM_TOKENS = {"team", "channel", "#", "@team", "engineering", "everyone"}
REQUIRED = ["title", "owner", "trigger", "output_shape", "conclusion", "reversal_clause", "review"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    owner = obj.get("owner", "")
    if isinstance(owner, str):
        low = owner.lower()
        if not owner or any(t in low for t in TEAM_TOKENS):
            errs.append("owner must be a named person, not a team/channel")
    trig = obj.get("trigger")
    if isinstance(trig, dict):
        if trig.get("kind") not in KINDS:
            errs.append("trigger.kind must be in {threshold, event, schedule}")
        if trig.get("threshold") is None:
            errs.append("trigger.threshold must be a number, not null")
        if not trig.get("window"):
            errs.append("trigger.window must be non-empty")
        if not trig.get("metric"):
            errs.append("trigger.metric must be non-empty")
    elif "trigger" in obj:
        errs.append("trigger must be object")
    if not obj.get("output_shape"):
        errs.append("output_shape must be non-empty (free-form output forbidden)")
    if not obj.get("reversal_clause"):
        errs.append("reversal_clause must be non-empty")
    concl = obj.get("conclusion")
    if isinstance(concl, dict):
        evs = concl.get("evidence_links")
        if not isinstance(evs, list) or len(evs) < 1:
            errs.append("conclusion.evidence_links must have >=1 entry")
    elif "conclusion" in obj:
        errs.append("conclusion must be object")
    rev = obj.get("review")
    if isinstance(rev, dict):
        if rev.get("cadence") not in CADENCES:
            errs.append("review.cadence must be monthly or quarterly")
        if not rev.get("last_run_at"):
            errs.append("review.last_run_at must be filled")
    elif "review" in obj:
        errs.append("review must be object")
    return errs


OK = {
    "title": "Faion Pro quit-day-job contract",
    "owner": "Ruslan",
    "trigger": {"kind": "threshold", "metric": "mrr_usd", "threshold": 4000, "window": "3 consecutive months above"},
    "output_shape": "decision-record stored at .product/decisions/quit-day-job.md",
    "conclusion": {
        "statement": "Resign on the first of the month after 3rd consecutive month >= $4000 MRR and >= 12 months runway.",
        "evidence_links": ["https://stripe.com/dashboard", "https://faion.net/runway-2026-Q2"],
    },
    "reversal_clause": "Return to W-2 if MRR drops below $3000 for 2 consecutive months OR runway falls below 6 months.",
    "review": {"cadence": "quarterly", "last_run_at": "2026-05-23"},
    "version": "1.0.0",
}
BAD = {
    "title": "draft contract",
    "owner": "team",
    "trigger": {"kind": "feeling", "metric": "ready", "threshold": None, "window": "when needed"},
    "output_shape": "",
    "conclusion": {"statement": "quit when ready", "evidence_links": []},
    "reversal_clause": "",
    "review": {"cadence": "ad-hoc", "last_run_at": ""},
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
