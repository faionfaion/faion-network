#!/usr/bin/env python3
"""validate-pivot-vs-quit-decision-template.py

Validate the artefact produced by the `pivot-vs-quit-decision-template` methodology against the JSON Schema embedded in
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

REQUIRED = ["decision_id", "owner", "last_touched", "current_state", "pivot_option", "quit_option", "criteria_scores", "decision", "rationale"]
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


OK = json.loads(r"""{"decision_id": "pivot-quit-acme-2026q2", "owner": "alex@acme.io", "last_touched": "2026-05-23T11:00:00Z", "current_state": {"weekly_active": 28, "mrr": 410, "runway_months": 8, "evidence": "BI snapshot 2026-05-22 + bank 2026-05-22"}, "pivot_option": {"description": "Reposition to enterprise procurement teams", "hypothesis": "10 procurement teams pre-pay $500/mo within 60 days", "evidence": "3 procurement interviews 2026-05"}, "quit_option": {"description": "Refund all paid users + open-source codebase + sunset domain", "cost": "$2,100 refunds + 2 weeks of cleanup", "evidence": "Stripe refund estimate 2026-05-22"}, "criteria_scores": {"customer_pull_pivot": 3, "customer_pull_quit": 0, "founder_energy": 3, "runway_fit_pivot": 4, "runway_fit_quit": 5}, "decision": "pivot", "rationale": "procurement signal strong + runway fits 60-day test", "template_version": "1.1.0", "status": "ready_for_review"}""")
BAD = json.loads(r"""{"decision_id": "x", "decision": "vibes", "criteria_scores": {}}""")


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
