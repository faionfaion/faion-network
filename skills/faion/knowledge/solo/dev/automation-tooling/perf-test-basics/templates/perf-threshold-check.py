#!/usr/bin/env python3
"""CI script: parse load-test JSON results and exit 1 on threshold breach.

Input: path to JSON results file (k6 summary or Locust stats).
Output: pass/fail per metric printed to stdout; exits 1 on any breach.

Usage:
    python perf-threshold-check.py results/summary.json
"""
import json
import sys


THRESHOLDS = {
    "http_req_duration_p95": 500,  # p95 < 500ms
    "http_req_failed_rate": 0.01,  # error rate < 1%
    "http_reqs_rate": 100,         # throughput >= 100 req/s
}


def check_results(results_file: str) -> bool:
    with open(results_file) as f:
        results = json.load(f)

    metrics = results.get("metrics", {})
    passed = True

    for metric, threshold in THRESHOLDS.items():
        actual = metrics.get(metric, {}).get("value", 0)
        is_rate_upper = "failed" in metric
        is_lower_bound = "rate" in metric and "failed" not in metric

        if is_rate_upper:
            ok = actual <= threshold
        elif is_lower_bound:
            ok = actual >= threshold
        else:
            ok = actual <= threshold  # latency: lower is better

        status = "PASS" if ok else "FAIL"
        print(f"{metric}: {actual:.2f} (threshold: {threshold}) [{status}]")
        if not ok:
            passed = False

    return passed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: perf-threshold-check.py <results.json>")
        sys.exit(2)
    if not check_results(sys.argv[1]):
        sys.exit(1)
