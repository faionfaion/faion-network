#!/usr/bin/env python3
"""validate-retainer-renewal-decision-rule.py

Validate a RetainerDecision JSON against content/02-output-contract.xml. Stdlib-only.

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
import re
import sys
from pathlib import Path

QUARTER_RX = re.compile(r"^[0-9]{4}-Q[1-4]$")
DECISIONS = {"keep", "upsell", "renegotiate", "kill"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("client_id", "quarter", "header", "inputs", "thresholds", "decision", "evidence", "review_log"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    if not QUARTER_RX.match(obj["quarter"]):
        errs.append("quarter must match YYYY-Qn")
    h = obj["header"]
    if not h.get("owner", {}).get("person"):
        errs.append("header.owner.person empty (rule: r4-recorded-call)")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days (rule: r5-review-on-failure)")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    inputs = obj["inputs"]
    for k in ("realised_margin_pct", "utilisation_pct", "nps", "strategic_fit"):
        if k not in inputs or not isinstance(inputs[k], (int, float)):
            errs.append(f"inputs.{k} missing/non-numeric (rule: r1-named-inputs)")

    thr = obj["thresholds"]
    for k in ("margin_min", "utilisation_max", "nps_min", "strategic_fit_min"):
        if not isinstance(thr.get(k), (int, float)):
            errs.append(f"thresholds.{k} must be numeric (rule: r2-published-thresholds)")

    if obj["decision"] not in DECISIONS:
        errs.append(f"decision invalid (rule: r3-default-action)")
    if not obj["evidence"]:
        errs.append("evidence empty (rule: r4-recorded-call)")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "client_id": "x", "quarter": "2026-Q2",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01", "version": "0"},
    "inputs": {"realised_margin_pct": 5, "utilisation_pct": 95, "nps": 10, "strategic_fit": 2},
    "thresholds": {"margin_min": "good", "utilisation_max": "fine", "nps_min": "ok", "strategic_fit_min": 3},
    "decision": "keep_because_client_likes_us",
    "evidence": [], "review_log": []
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
