#!/usr/bin/env python3
"""perf-gate.py — fail if metrics regress vs baseline.

Input:  sys.argv[1] = current results JSON (k6 summary format)
        sys.argv[2] = baseline results JSON
        sys.argv[3] = tolerance fraction (default 0.05 = 5%)
Output: stdout lines with metric/status, exit 1 on any regression
"""
import json
import sys
from pathlib import Path


def compare(current: Path, baseline: Path, tol: float = 0.05) -> int:
    cur = json.loads(current.read_text())["metrics"]
    base = json.loads(baseline.read_text())["metrics"]
    fail = 0
    keys = ["http_req_duration_p95", "http_req_failed_rate"]
    for k in keys:
        c = cur.get(k, {}).get("value", 0)
        b = base.get(k, {}).get("value", 0)
        if b == 0:
            continue
        delta = (c - b) / b
        flag = "REGRESS" if delta > tol else "OK"
        if flag == "REGRESS":
            fail += 1
        print(f"{k}: cur={c:.2f} base={b:.2f} delta={delta:+.1%} {flag}")
    return 1 if fail else 0


if __name__ == "__main__":
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
    sys.exit(compare(Path(sys.argv[1]), Path(sys.argv[2]), tol))
