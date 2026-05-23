#!/usr/bin/env python3
"""perf-gate.py — fail if metrics regress vs baseline.

Inputs:
    --current PATH    current results JSON (k6 summary format)
    --baseline PATH   baseline results JSON
    --tolerance FLOAT regression tolerance fraction (default 0.05 = 5%)
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = no regression
    1 = regression detected (per-metric report on stdout)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path


METRIC_KEYS = ["http_req_duration_p95", "http_req_failed_rate"]


def compare(current: Path, baseline: Path, tol: float = 0.05) -> int:
    try:
        cur = json.loads(current.read_text())["metrics"]
        base = json.loads(baseline.read_text())["metrics"]
    except (OSError, json.JSONDecodeError, KeyError) as e:
        sys.stderr.write(f"could not load metrics: {e}\n")
        return 2
    fail = 0
    for k in METRIC_KEYS:
        c = cur.get(k, {}).get("value", 0)
        b = base.get(k, {}).get("value", 0)
        if b == 0:
            continue
        delta = (c - b) / b
        flag = "REGRESS" if delta > tol else "OK"
        if flag == "REGRESS":
            fail += 1
        sys.stdout.write(f"{k}: cur={c:.2f} base={b:.2f} delta={delta:+.1%} {flag}\n")
    return 1 if fail else 0


def self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        cur = Path(td) / "cur.json"
        base = Path(td) / "base.json"
        # No regression
        base.write_text(json.dumps({"metrics": {
            "http_req_duration_p95": {"value": 100.0},
            "http_req_failed_rate": {"value": 0.01},
        }}))
        cur.write_text(json.dumps({"metrics": {
            "http_req_duration_p95": {"value": 102.0},
            "http_req_failed_rate": {"value": 0.01},
        }}))
        rc = compare(cur, base, 0.05)
        if rc != 0:
            sys.stderr.write("self-test: no-regress fixture flagged regress\n")
            return 1
        # Regression
        cur.write_text(json.dumps({"metrics": {
            "http_req_duration_p95": {"value": 150.0},
            "http_req_failed_rate": {"value": 0.01},
        }}))
        rc = compare(cur, base, 0.05)
        if rc != 1:
            sys.stderr.write("self-test: regress fixture not flagged\n")
            return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--current", type=str, help="current results JSON")
    ap.add_argument("--baseline", type=str, help="baseline results JSON")
    ap.add_argument("--tolerance", type=float, default=0.05, help="regression tolerance (default 0.05)")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.current and args.baseline):
        ap.print_help()
        return 2
    return compare(Path(args.current), Path(args.baseline), args.tolerance)


if __name__ == "__main__":
    sys.exit(main())
