#!/usr/bin/env python3
"""validate-pr-time-cost-diff-tool.py — validate the cost-report artefact.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["pr_number", "base_sha", "head_sha", "eval_set_hash", "cost_table_version", "deltas", "verdict"]
DELTA_KEYS = ["median_latency_ms", "p95_latency_ms", "usd_per_req_cents", "eval_pass_rate_pct"]
VERDICT_ENUM = {"pass", "fail", "warn"}

VALID_FIXTURE = {
    "pr_number": 482,
    "base_sha": "a1b2c3d",
    "head_sha": "e4f5a6b",
    "eval_set_hash": "1234567",
    "cost_table_version": "2026.05.20",
    "deltas": {"median_latency_ms": 12, "p95_latency_ms": 80, "usd_per_req_cents": 0.3, "eval_pass_rate_pct": -0.5},
    "verdict": "pass",
    "budget_breach_reasons": [],
}

INVALID_FIXTURE = {
    "pr_number": 482,
    "deltas": {"usd_per_req_cents": 0.3},
    "verdict": "ok",
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    deltas = obj.get("deltas", {})
    if not isinstance(deltas, dict):
        errs.append("deltas: must be object")
    else:
        for k in DELTA_KEYS:
            if k not in deltas:
                errs.append(f"deltas: missing {k}")
            elif not isinstance(deltas[k], (int, float)) or isinstance(deltas[k], bool):
                errs.append(f"deltas.{k}: must be number")
    v = obj.get("verdict")
    if v not in VERDICT_ENUM:
        errs.append(f"verdict: {v!r} not in {sorted(VERDICT_ENUM)}")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
