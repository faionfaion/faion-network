#!/usr/bin/env python3
"""validate-regulatory-uncertainty-buffer.py

Validate a RegulatoryBuffer JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to buffer JSON
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

ACTIONS = {"proceed", "pause", "escalate_to_legal"}
VAGUE_SIGNALS = {"use judgment", "significant", "material", "tbd"}
VAGUE_THRESHOLDS = {"significant", "material", "high", "low"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("project_id", "header", "rules", "review_log"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
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

    for i, r in enumerate(obj["rules"]):
        for k in ("rule_id", "jurisdiction", "regulation", "signal", "threshold", "default_action", "buffer_pct", "evidence"):
            if k not in r:
                errs.append(f"rules[{i}].{k} missing")
        if (r.get("signal") or "").lower() in VAGUE_SIGNALS:
            errs.append(f"rules[{i}].signal vague (rule: r1-named-inputs)")
        thr = r.get("threshold")
        if not isinstance(thr, (int, float, bool)):
            errs.append(f"rules[{i}].threshold must be numeric/boolean (rule: r2-published-thresholds)")
        if str(thr).lower() in VAGUE_THRESHOLDS:
            errs.append(f"rules[{i}].threshold vague (rule: r2-published-thresholds)")
        if r.get("default_action") not in ACTIONS:
            errs.append(f"rules[{i}].default_action invalid (rule: r3-default-action)")
        if not r.get("evidence"):
            errs.append(f"rules[{i}].evidence empty (rule: r4-recorded-call)")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "project_id": "x",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01", "version": "0"},
    "rules": [{"rule_id": "r1", "jurisdiction": "EU", "regulation": "AI Act",
               "signal": "use judgment", "threshold": "significant",
               "default_action": "guess", "buffer_pct": 30, "evidence": []}],
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
