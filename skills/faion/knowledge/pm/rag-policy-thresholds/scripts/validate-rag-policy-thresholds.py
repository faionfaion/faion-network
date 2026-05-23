#!/usr/bin/env python3
"""validate-rag-policy-thresholds.py

Validate a RAGPolicy JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to policy JSON
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

TRIGGERS = {"weekly_status", "fortnightly_status", "monthly_status"}
COMPARATORS = {"gt", "lt", "gte", "lte", "eq"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("project_id", "header", "signals", "actions", "review_log"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    h = obj["header"]
    if h.get("trigger") not in TRIGGERS:
        errs.append("header.trigger invalid (rule: r1-explicit-trigger)")
    if not h.get("owner", {}).get("person"):
        errs.append("header.owner.person empty (rule: r4-named-owner)")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days (rule: r5-iteration-loop)")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    for i, s in enumerate(obj["signals"]):
        for k in ("signal_id", "input_source", "amber_threshold", "red_threshold", "comparator", "evidence"):
            if k not in s:
                errs.append(f"signals[{i}].{k} missing")
        if not isinstance(s.get("amber_threshold"), (int, float)):
            errs.append(f"signals[{i}].amber_threshold must be numeric (rule: r2-bounded-output)")
        if not isinstance(s.get("red_threshold"), (int, float)):
            errs.append(f"signals[{i}].red_threshold must be numeric (rule: r2-bounded-output)")
        if s.get("comparator") not in COMPARATORS:
            errs.append(f"signals[{i}].comparator invalid")
        if not s.get("evidence"):
            errs.append(f"signals[{i}].evidence empty (rule: r3-evidence-anchored)")

    actions = obj["actions"]
    for c in ("green", "amber", "red"):
        if c not in actions:
            errs.append(f"actions.{c} missing")
    if len(actions.get("amber", "")) < 10:
        errs.append("actions.amber too short (rule: r4-named-owner)")
    if len(actions.get("red", "")) < 10:
        errs.append("actions.red too short (rule: r4-named-owner)")

    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "project_id": "x",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01",
               "version": "0", "trigger": "when_needed", "reporting_cadence_days": 7},
    "signals": [{"signal_id": "s", "input_source": "guess",
                 "amber_threshold": "significant", "red_threshold": "material",
                 "comparator": "gt", "evidence": []}],
    "actions": {"green": "", "amber": "x", "red": "y"},
    "review_log": []
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
