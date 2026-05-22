#!/usr/bin/env python3
"""validate-thumbs-down-to-eval-pipeline.py — validate EvalCandidate JSON.

Inputs:
    --file PATH    JSON file to validate
    --self-test    Run built-in fixtures
    --help         Show this message

Exit codes:
    0  valid
    1  invalid
    2  usage error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = [
    "interaction_id", "prompt", "response", "signal", "timestamp",
    "pii_clean", "judge_votes", "cluster_size", "admitted_this_week",
]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("signal") not in ("down", "report"):
        errs.append("signal must be 'down' or 'report'")
    if obj.get("pii_clean") is not True:
        errs.append("pii_clean must be true to enter admit pipeline (r2-pii-scrub-gate)")
    votes = obj.get("judge_votes", [])
    if not isinstance(votes, list) or len(votes) != 3:
        errs.append("judge_votes must be a list of exactly 3 (r3-three-judge-vote)")
    if obj.get("admitted_this_week", 0) > 50:
        errs.append("admitted_this_week exceeds weekly cap of 50 (r4-weekly-cap)")
    if obj.get("cluster_size", 0) < 1:
        errs.append("cluster_size must be >= 1")
    return errs


FIXTURE_VALID = {
    "interaction_id": "i-001",
    "prompt": "p",
    "response": "r",
    "signal": "down",
    "timestamp": "2026-05-22T14:32:00Z",
    "pii_clean": True,
    "judge_votes": ["ADMIT", "ADMIT", "REJECT"],
    "cluster_size": 3,
    "admitted_this_week": 12,
}

FIXTURE_INVALID = {
    "interaction_id": "i-002",
    "prompt": "p",
    "response": "r",
    "signal": "up",
    "timestamp": "2026-05-22T14:32:00Z",
    "pii_clean": False,
    "judge_votes": ["ADMIT"],
    "cluster_size": 0,
    "admitted_this_week": 99,
}


def self_test() -> int:
    if validate(FIXTURE_VALID):
        sys.stderr.write("valid fixture rejected\n")
        return 1
    errs = validate(FIXTURE_INVALID)
    if not errs:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write(f"self-test OK ({len(errs)} violations on invalid)\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-thumbs-down-to-eval-pipeline",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
