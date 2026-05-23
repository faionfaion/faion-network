#!/usr/bin/env python3
"""validate-founder-deal-kill-rule.py

Validate one kill-batch JSON against the schema.

Inputs:
    --file PATH       path to JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid; 1 = invalid; 2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
BID = re.compile(r"^kb-\d{4}-\d{2}-\d{2}$")
TRIPS = {"no_reply", "last_meeting", "missed_milestone", "budget_unconfirmed", "champion_left"}
ACTIONS = {"killed", "kept", "escalated"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("batch_id", "run_date", "owner", "thresholds", "deals", "killed", "escalated"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    if not BID.match(obj.get("batch_id", "")):
        errs.append("batch_id must match kb-YYYY-MM-DD")
    owner = obj.get("owner", "")
    if not owner or len(owner) < 3 or BANNED.match(owner.strip()):
        errs.append(f"owner invalid: {owner!r}")
    th = obj.get("thresholds") or {}
    for nk in ("no_reply_days", "last_meeting_days"):
        if nk not in th or not isinstance(th[nk], int):
            errs.append(f"thresholds.{nk} missing or not int")
    deals = obj.get("deals") or []
    if not isinstance(deals, list):
        errs.append("deals must be array")
    for i, d in enumerate(deals if isinstance(deals, list) else []):
        trips = d.get("trips") or []
        if not isinstance(trips, list):
            errs.append(f"deals[{i}].trips must be array")
        for t in trips:
            if t not in TRIPS:
                errs.append(f"deals[{i}].trips contains invalid: {t!r}")
        a = d.get("action")
        if a not in ACTIONS:
            errs.append(f"deals[{i}].action invalid: {a!r}")
        if len(trips) >= 2 and a not in {"killed", "escalated"}:
            errs.append(f"deals[{i}] has {len(trips)} trips but action={a} (rule two-trip-auto-kill)")
        rw = d.get("reversal_window_days")
        if rw is not None and (not isinstance(rw, int) or rw < 0 or rw > 30):
            errs.append(f"deals[{i}].reversal_window_days must be 0..30 (rule reversible-30-days)")
    return errs


OK = {
    "batch_id": "kb-2026-05-23", "run_date": "2026-05-23", "owner": "@ruslan",
    "thresholds": {"no_reply_days": 21, "last_meeting_days": 30},
    "deals": [
        {"deal_id": "d-101", "trips": ["no_reply", "last_meeting"], "action": "killed", "reversal_window_days": 30},
        {"deal_id": "d-102", "trips": ["budget_unconfirmed"], "action": "kept"},
    ],
    "killed": 1, "escalated": 0,
}
BAD = {"batch_id": "kb-1", "owner": "team", "thresholds": {"no_reply_days": "stale"}, "deals": [], "killed": 0, "escalated": 0, "run_date": "2026-05-23"}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write(f"ok rejected: {validate(OK)}\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
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
        ap.print_help()
        return 2
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
