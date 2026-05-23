#!/usr/bin/env python3
"""validate-solo-late-fee-and-pause-clause-template.py

Validate a LateFeeClauseSpec JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to spec JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("spec_id", "jurisdiction", "header", "late_fee_tiers",
             "pause_days", "re_engagement_fee_usd", "jurisdiction_review", "clause_text"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    h = obj["header"]
    if not h.get("owner", {}).get("person"):
        errs.append("header.owner.person empty")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    if obj["pause_days"] < 14:
        errs.append(f"pause_days {obj['pause_days']} < 14 (rule: r3-pause-after-14-days)")
    if obj["re_engagement_fee_usd"] <= 0:
        errs.append("re_engagement_fee_usd must be > 0 (rule: r4-re-engagement-fee)")
    if len(obj["clause_text"]) < 100:
        errs.append("clause_text too short (rule: r1-clause-in-sow-not-email)")
    if obj["clause_text"].lower().strip() in {"see email", "in email"}:
        errs.append("clause_text references email (rule: r1-clause-in-sow-not-email)")

    tiers = obj["late_fee_tiers"]
    if len(tiers) < 2:
        errs.append("late_fee_tiers must have >= 2 escalating tiers (rule: r2-late-fee-tiered)")
    if tiers:
        sorted_tiers = sorted(tiers, key=lambda t: t["after_days"])
        for i in range(1, len(sorted_tiers)):
            if sorted_tiers[i]["rate_pct_per_month"] <= sorted_tiers[i-1]["rate_pct_per_month"]:
                errs.append(f"late_fee_tiers must escalate (rule: r2-late-fee-tiered)")
                break

    jr = obj["jurisdiction_review"]
    if not jr.get("reviewed_by") or not jr.get("memo_link"):
        errs.append("jurisdiction_review.reviewed_by + memo_link required (rule: r5-jurisdiction-review)")
    try:
        rd = dt.date.fromisoformat(jr.get("reviewed_at", ""))
        if (dt.date.today() - rd).days > 366:
            errs.append("jurisdiction_review > 12 months old (rule: r5-jurisdiction-review)")
    except Exception:
        errs.append("jurisdiction_review.reviewed_at not ISO date")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "spec_id": "x", "jurisdiction": "?",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01", "version": "0"},
    "late_fee_tiers": [{"after_days": 30, "rate_pct_per_month": 1.5}],
    "pause_days": 7,
    "re_engagement_fee_usd": 0,
    "jurisdiction_review": {"reviewed_by": "", "reviewed_at": "2024-01-01", "memo_link": ""},
    "clause_text": "see email"
}


def self_test() -> int:
    if SMOKE_OK_FILE.is_file():
        ok = json.loads(SMOKE_OK_FILE.read_text())
        today = dt.date.today()
        ok["header"]["last_reviewed"] = today.isoformat()
        ok["jurisdiction_review"]["reviewed_at"] = today.isoformat()
        errs = validate(ok)
        if errs:
            sys.stderr.write("smoke_ok rejected: " + "; ".join(errs) + "\n"); return 1
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
