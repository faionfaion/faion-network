#!/usr/bin/env python3
"""validate-retainer-vs-project-rubric.py

Validate an EngagementRubric JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to rubric JSON
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

RECS = {"retainer", "project", "hybrid", "decline"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("opportunity_id", "header", "dimensions", "aggregate_score", "recommendation"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    h = obj["header"]
    if not h.get("owner", {}).get("person"):
        errs.append("header.owner.person empty")
    if len(h.get("reviewers", [])) < 2:
        errs.append("header.reviewers must have >= 2 entries (rule: r4-calibration-pass)")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days (rule: r5-versioned)")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    dims = obj["dimensions"]
    if not (4 <= len(dims) <= 7):
        errs.append(f"dimensions count {len(dims)} not in [4,7] (rule: r1-named-dimensions)")
    for i, d in enumerate(dims):
        if not isinstance(d.get("score"), int) or not (1 <= d["score"] <= 5):
            errs.append(f"dimensions[{i}].score must be int 1-5")
        if "subjective overall" in (d.get("name", "")).lower():
            errs.append(f"dimensions[{i}] uses subjective-overall dimension (rule: r1-named-dimensions)")
        if not d.get("evidence"):
            errs.append(f"dimensions[{i}].evidence empty (rule: r2-evidence-per-score)")
        if len(d.get("anchor_text", "")) < 10:
            errs.append(f"dimensions[{i}].anchor_text too short")

    if obj["recommendation"] not in RECS:
        errs.append(f"recommendation invalid (rule: r3-aggregation-rule)")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "opportunity_id": "x",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01", "version": "0", "reviewers": ["one"]},
    "dimensions": [{"dimension_id": "subj", "name": "subjective overall", "score": 3, "anchor_text": "ok", "evidence": ""}],
    "aggregate_score": 3,
    "recommendation": "good"
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
