#!/usr/bin/env python3
"""validate-trajectory-eval-otel.py

Validate a trajectory-eval report JSON against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to eval-report JSON
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
import sys
from pathlib import Path

VERDICTS = {"pass", "regress-outcome", "regress-trajectory", "regress-resources"}
AXES = ("outcome", "trajectory", "resources")
RAW_KEYS = ("total_tokens", "total_cost_usd", "total_steps", "total_latency_ms")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("run_id", "task_id", "scores", "raw", "verdict"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    scores = obj.get("scores") or {}
    for ax in AXES:
        v = scores.get(ax)
        if v is None:
            errs.append(f"scores missing {ax}")
        elif not (isinstance(v, (int, float)) and 0 <= v <= 1):
            errs.append(f"scores.{ax} must be number in [0,1]")
    raw = obj.get("raw") or {}
    for k in RAW_KEYS:
        if k not in raw:
            errs.append(f"raw missing {k}")
        elif not isinstance(raw[k], (int, float)) or raw[k] < 0:
            errs.append(f"raw.{k} must be >= 0")
    if obj.get("verdict") not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")
    return errs


OK = {
    "run_id": "run-1", "task_id": "t-1",
    "scores": {"outcome": 1.0, "trajectory": 0.78, "resources": 0.85},
    "raw": {"total_tokens": 8200, "total_cost_usd": 0.04, "total_steps": 4, "total_latency_ms": 12000},
    "verdict": "pass",
}
BAD = {"scores": {"outcome": 1.0}}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n"); return 1
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
