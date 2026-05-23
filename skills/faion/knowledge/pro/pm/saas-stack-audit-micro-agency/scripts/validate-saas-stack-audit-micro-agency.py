#!/usr/bin/env python3
"""validate-saas-stack-audit-micro-agency.py

Validate a SaaSAuditReport JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to audit JSON
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
import re
import sys
from pathlib import Path

QUARTER_RX = re.compile(r"^[0-9]{4}-Q[1-4]$")
BUCKETS = {"keep", "consolidate", "downgrade_seat", "suspend", "cancel"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("audit_id", "quarter", "header", "inventory", "kill_list", "spend_before", "spend_forecast_after", "review_log"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    if not QUARTER_RX.match(obj["quarter"]):
        errs.append("quarter must match YYYY-Qn")
    h = obj["header"]
    if not h.get("owner", {}).get("person"):
        errs.append("header.owner.person empty")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days (rule: r5-savings-tracked-next-quarter)")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    inv = obj["inventory"]
    if len(inv) < 5:
        errs.append(f"inventory length {len(inv)} < 5 (rule: r1-full-stack-inventory)")
    for i, t in enumerate(inv):
        if t.get("bucket") not in BUCKETS:
            errs.append(f"inventory[{i}].bucket invalid")
        if t.get("bucket") == "keep":
            if not t.get("tied_to_revenue") and not t.get("evidence"):
                errs.append(f"inventory[{i}] keep without revenue tie + evidence (rule: r3-evidence-required-to-keep)")

    kl = obj["kill_list"]
    if not kl.get("signed_by"):
        errs.append("kill_list.signed_by empty (rule: r4-kill-list-signed)")

    if obj["kill_list"]["items"] and obj["spend_forecast_after"] >= obj["spend_before"]:
        errs.append("spend_forecast_after >= spend_before despite non-empty kill_list (math inconsistent)")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "audit_id": "x", "quarter": "2026-Q2",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01", "version": "0"},
    "inventory": [{"tool_id": "x", "vendor": "x", "monthly_cost_usd": 100, "last_login_days": 200,
                   "tied_to_revenue": False, "duplicate_of": None, "bucket": "keep", "evidence": []}],
    "kill_list": {"items": [], "signed_by": "", "signed_at": "2026-05-10"},
    "spend_before": 100, "spend_forecast_after": 100, "review_log": []
}


def self_test() -> int:
    if SMOKE_OK_FILE.is_file():
        ok = json.loads(SMOKE_OK_FILE.read_text())
        ok["header"]["last_reviewed"] = dt.date.today().isoformat()
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
