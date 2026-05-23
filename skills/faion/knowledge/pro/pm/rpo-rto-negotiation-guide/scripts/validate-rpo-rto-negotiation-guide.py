#!/usr/bin/env python3
"""validate-rpo-rto-negotiation-guide.py

Validate an AcceptanceRecord JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to record JSON
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
    for k in ("record_id", "system_id", "header", "options_presented", "chosen",
             "impact_basis", "stakeholder_handle", "evidence_link", "decided_at", "refresh_due"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    opts = obj["options_presented"]
    if not isinstance(opts, list) or len(opts) < 3:
        errs.append(f"options_presented length {len(opts) if isinstance(opts, list) else '?'} < 3 (rule: r3-tier-banded-options)")

    chosen = obj["chosen"]
    if not chosen.get("stakeholder_echo") or len(chosen["stakeholder_echo"]) < 10:
        errs.append("chosen.stakeholder_echo empty/too short (rule: r1-stakeholder-owns-number)")

    if len(obj.get("impact_basis", "")) < 20:
        errs.append("impact_basis too short (rule: r2-impact-before-cost)")

    if not obj.get("evidence_link"):
        errs.append("evidence_link empty (rule: r4-signed-acceptance-record)")

    try:
        decided = dt.date.fromisoformat(obj["decided_at"])
        refresh = dt.date.fromisoformat(obj["refresh_due"])
        delta_days = (refresh - decided).days
        if delta_days > 366:
            errs.append(f"refresh_due {delta_days} days after decided_at > 12 months (rule: r5-refresh-cadence)")
        if delta_days <= 0:
            errs.append("refresh_due must be after decided_at")
    except Exception:
        errs.append("decided_at or refresh_due not ISO date")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "record_id": "x", "system_id": "x",
    "header": {"owner": {"role": "team", "person": ""}, "version": "0"},
    "options_presented": [{"tier_name": "only", "rpo": "1h", "rto": "1h", "annual_cost_delta": "?", "operational_impact": "ok"}],
    "chosen": {"tier_name": "only", "rpo": "1h", "rto": "1h", "stakeholder_echo": ""},
    "impact_basis": "tbd",
    "stakeholder_handle": "",
    "evidence_link": "",
    "decided_at": "2026-05-20",
    "refresh_due": "2030-05-20"
}


def self_test() -> int:
    if SMOKE_OK_FILE.is_file():
        ok = json.loads(SMOKE_OK_FILE.read_text())
        # rebase decided_at + refresh_due to today
        today = dt.date.today()
        ok["decided_at"] = today.isoformat()
        ok["refresh_due"] = (today + dt.timedelta(days=365)).isoformat()
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
