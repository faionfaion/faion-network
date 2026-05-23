#!/usr/bin/env python3
"""validate-retro-format-rotation-guide.py

Validate the rotation guide artefact against the JSON Schema in
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

FORMATS = {"start-stop-continue", "sailboat", "4ls", "timeline", "anonymous-async", "mad-sad-glad", "lean-coffee"}
DISTRIBUTIONS = {"async", "hybrid", "in-person"}
FATIGUE = {"fresh", "rotating", "fatigued"}
CADENCES = {"next-retro", "monthly", "quarterly"}
TEAM_TOKENS = {"team", "channel", "#", "@team", "everyone"}
REQUIRED = ["team_id", "owner", "last_3_formats", "next_format", "rationale", "team_state", "outcome_review"]


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
            errs.append("owner must be a named person")
    lf = obj.get("last_3_formats")
    if isinstance(lf, list):
        if len(lf) != 3:
            errs.append("last_3_formats must have exactly 3 entries")
        for i, f in enumerate(lf):
            if f not in FORMATS:
                errs.append(f"last_3_formats[{i}] not in closed list")
    elif "last_3_formats" in obj:
        errs.append("last_3_formats must be array")
    nf = obj.get("next_format")
    if nf not in FORMATS:
        errs.append("next_format not in closed list")
    if isinstance(lf, list) and nf in lf:
        errs.append("next_format in last_3_formats (no-repeat rule)")
    if not isinstance(obj.get("rationale"), str) or len(obj.get("rationale", "")) < 20:
        errs.append("rationale must be non-empty and >=20 chars")
    ts = obj.get("team_state")
    if isinstance(ts, dict):
        if ts.get("distribution") not in DISTRIBUTIONS:
            errs.append("team_state.distribution not in enum")
        if ts.get("fatigue_signal") not in FATIGUE:
            errs.append("team_state.fatigue_signal not in enum")
    elif "team_state" in obj:
        errs.append("team_state must be object")
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
    "team_id": "platform",
    "owner": "Ruslan",
    "last_3_formats": ["mad-sad-glad", "4ls", "sailboat"],
    "next_format": "anonymous-async",
    "rationale": "Distribution shifted to async after Carol relocated to PT timezone; previous 3 covered in-person variants; rotate to async.",
    "team_state": {"distribution": "async", "fatigue_signal": "rotating"},
    "outcome_review": {"cadence": "next-retro", "last_run_at": "2026-05-09"},
}
BAD = {
    "team_id": "platform",
    "owner": "team",
    "last_3_formats": ["sailboat", "sailboat", "sailboat"],
    "next_format": "sailboat",
    "rationale": "everyone likes it",
    "team_state": {"distribution": "remote", "fatigue_signal": "tired"},
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
