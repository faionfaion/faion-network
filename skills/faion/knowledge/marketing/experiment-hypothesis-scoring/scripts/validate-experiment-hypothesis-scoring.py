#!/usr/bin/env python3
"""validate-experiment-hypothesis-scoring.py

Validate one scored-hypothesis JSON against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
HID = re.compile(r"^hyp-[a-z0-9-]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("hypothesis_id", "hypothesis", "rubric_version", "scores", "queued", "raters", "cycle_id"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    if not HID.match(obj.get("hypothesis_id", "")):
        errs.append("hypothesis_id must match hyp-<slug>")
    if not SEMVER.match(obj.get("rubric_version", "")):
        errs.append("rubric_version must be semver")
    if not isinstance(obj.get("hypothesis"), str) or len(obj.get("hypothesis", "")) < 20:
        errs.append("hypothesis too short")
    raters = obj.get("raters") or []
    if not isinstance(raters, list) or len(raters) < 2:
        errs.append("raters must have >=2 entries (rule two-rater-calibration)")
    scores = obj.get("scores") or {}
    for ax in ("impact", "confidence", "ease"):
        s = scores.get(ax) or {}
        b = s.get("band")
        if not isinstance(b, int) or not (1 <= b <= 5):
            errs.append(f"scores.{ax}.band missing or out of 1..5")
        ev = s.get("evidence", "")
        if not isinstance(ev, str) or len(ev) < 10:
            errs.append(f"scores.{ax}.evidence missing or <10 chars (rule evidence-required)")
    pl = scores.get("projected_lift_pct")
    if not isinstance(pl, (int, float)) or pl < 0:
        errs.append("scores.projected_lift_pct missing or negative")
    queued = obj.get("queued")
    if queued is True:
        conf = (scores.get("confidence") or {}).get("band", 0)
        if (pl is None) or (isinstance(pl, (int, float)) and pl < 5) or (isinstance(conf, int) and conf < 3):
            errs.append("queued=true but threshold not met (rule min-entry-threshold)")
    return errs


OK = {
    "hypothesis_id": "hyp-x", "hypothesis": "x" * 30, "rubric_version": "1.0.0", "cycle_id": "2026-Q2",
    "scores": {
        "impact": {"band": 4, "evidence": "evidence string"},
        "confidence": {"band": 4, "evidence": "evidence string"},
        "ease": {"band": 3, "evidence": "evidence string"},
        "projected_lift_pct": 8.0,
    },
    "raters": ["@a", "@b"], "discrepancy_resolved": True, "queued": True,
}
BAD = {"hypothesis_id": "hyp-x", "scores": {"impact": {"band": 5}}, "raters": ["@a"], "queued": True}


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
