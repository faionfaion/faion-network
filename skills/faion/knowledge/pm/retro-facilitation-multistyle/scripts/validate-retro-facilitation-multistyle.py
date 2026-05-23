#!/usr/bin/env python3
"""validate-retro-facilitation-multistyle.py

Validate the per-retro instance artefact against the JSON Schema in
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

FORMATS = {"mad-sad-glad", "4ls", "sailboat", "lean-coffee", "anonymous-async"}
DISTRIBUTIONS = {"async", "hybrid", "in-person"}
FATIGUE = {"fresh", "rotating", "fatigued"}
CADENCES = {"next-retro", "monthly", "quarterly"}
REQUIRED = ["retro_date", "format", "selection_rationale", "team_state", "action_items", "outcome_review"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    fmt = obj.get("format")
    if isinstance(fmt, str) and fmt.lower() not in FORMATS:
        errs.append("format must be in closed list of 5")
    sr = obj.get("selection_rationale", "")
    if not isinstance(sr, str) or len(sr) < 20:
        errs.append("selection_rationale must be non-empty and >=20 chars")
    ts = obj.get("team_state")
    if isinstance(ts, dict):
        if ts.get("distribution") not in DISTRIBUTIONS:
            errs.append("team_state.distribution not in enum")
        if ts.get("fatigue_signal") not in FATIGUE:
            errs.append("team_state.fatigue_signal not in enum")
    elif "team_state" in obj:
        errs.append("team_state must be object")
    ai = obj.get("action_items")
    if isinstance(ai, list):
        if len(ai) < 1:
            errs.append("action_items must have >=1 entry")
        for i, a in enumerate(ai):
            if not isinstance(a, dict):
                continue
            if not a.get("owner"):
                errs.append(f"action_items[{i}].owner missing")
            if not a.get("evidence_link"):
                errs.append(f"action_items[{i}].evidence_link missing")
    elif "action_items" in obj:
        errs.append("action_items must be array")
    rev = obj.get("outcome_review")
    if isinstance(rev, dict):
        if rev.get("cadence") not in CADENCES:
            errs.append("outcome_review.cadence not in enum")
        if not rev.get("last_run_at"):
            errs.append("outcome_review.last_run_at must be filled")
    elif "outcome_review" in obj:
        errs.append("outcome_review must be object")
    return errs


OK = {
    "retro_date": "2026-05-23",
    "format": "anonymous-async",
    "selection_rationale": "Team is split across UA/PT/UK timezones; live retros bias toward UK voices. Async anonymous brings outsource feedback in.",
    "team_state": {"distribution": "async", "fatigue_signal": "rotating"},
    "action_items": [
        {"text": "Move backend deploy window to 16:00 UTC", "owner": "Carol", "evidence_link": "https://github.com/org/repo/issues/482", "due_date": "2026-05-30"}
    ],
    "outcome_review": {"cadence": "next-retro", "last_run_at": "2026-05-09"},
}
BAD = {
    "retro_date": "2026-05-23",
    "format": "freeform",
    "selection_rationale": "",
    "team_state": {"distribution": "remote", "fatigue_signal": "tired"},
    "action_items": [],
    "outcome_review": {"cadence": "ad-hoc", "last_run_at": ""},
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
