#!/usr/bin/env python3
"""validate-freelancer-to-saas-time-box.py

Validate the artefact produced by the `freelancer-to-saas-time-box` methodology against the JSON Schema embedded in
`content/02-output-contract.xml`. Stdlib-only.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["spec_id", "owner", "last_touched", "weekly_hours", "abort_criteria", "boundary_rules", "milestones", "review_cadence"]
PLACEHOLDERS = {"TBD", "TODO", "FIXME"}


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        v = obj[k]
        if v in (None, "", [], {}):
            errs.append(f"required field empty: {k}")
        if isinstance(v, str) and v.strip().upper() in PLACEHOLDERS:
            errs.append(f"placeholder value in field: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.lower().strip() in {"team", "we", "tbd"}:
        errs.append("owner must be a single named person, not 'team' / 'we' / 'TBD'")
    return errs


OK = json.loads(r"""{"spec_id": "fstx-jane-2026q2", "owner": "jane@indie.io", "last_touched": "2026-05-23T09:00:00Z", "weekly_hours": {"mon": 0, "tue": 3, "wed": 0, "thu": 3, "fri": 0, "sat": 2, "sun": 0, "evidence": "calendar export 2026-04 to 2026-05"}, "abort_criteria": [{"name": "no paying customer by day 60", "metric": "paid_signups", "threshold": 1, "evidence": "milestone roadmap"}], "boundary_rules": [{"rule": "no client work on Tuesday/Thursday/Saturday SaaS blocks", "consequence": "decline + reschedule"}], "milestones": [{"day": 30, "deliverable": "landing + payment link live"}, {"day": 60, "deliverable": "1 paid signup"}, {"day": 90, "deliverable": "5 paid signups OR abort"}], "review_cadence": "weekly Friday 30-min self-review", "template_version": "1.1.0", "status": "ready_for_review"}""")
BAD = json.loads(r"""{"spec_id": "x", "weekly_hours": {"mon": 80}, "abort_criteria": []}""")


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"valid fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
