#!/usr/bin/env python3
"""
variance.py — compute variance, statistical significance, and status for business metrics.

Usage:
    python variance.py metrics.json

Input (metrics.json):
    [
      {
        "name": "lead_conversion",
        "baseline": 0.10,
        "target": 0.12,
        "actual": 0.118,
        "n_baseline": 1000,
        "n_actual": 1150
      }
    ]

Output: table with variance %, z-test p-value, and status.
Status thresholds: variance >= 0% = met, -15..0% = partial, < -15% = not_met.
If p > 0.05 for a "met" verdict, the result is underpowered — escalate.
"""
import json
import math
import sys

from scipy import stats


def compute_status(target: float, actual: float, baseline: float) -> str:
    if target == baseline:
        return "met" if actual >= target else "not_met"
    progress = (actual - baseline) / (target - baseline)
    if progress >= 1.0:
        return "exceeded"
    if progress >= 0.85:
        return "on_track"
    if progress >= 0.5:
        return "at_risk"
    return "off_track"


def variance_pct(actual: float, target: float) -> float:
    if target == 0:
        return 0.0
    return (actual - target) / abs(target) * 100


def two_prop_z(p1: float, p2: float, n1: int, n2: int) -> float:
    """Two-proportion z-test p-value (two-tailed)."""
    pooled = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    if se == 0:
        return 1.0
    z = (p2 - p1) / se
    return float(2 * (1 - stats.norm.cdf(abs(z))))


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python variance.py metrics.json", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        rows = json.load(f)

    header = f"{'metric':<28}{'baseline':>10}{'target':>10}{'actual':>10}{'var%':>8}{'p':>8}  status"
    print(header)
    print("-" * len(header))

    for r in rows:
        var = variance_pct(r["actual"], r["target"])
        p = two_prop_z(r["baseline"], r["actual"], r["n_baseline"], r["n_actual"])
        status = compute_status(r["target"], r["actual"], r["baseline"])
        underpowered = " [UNDERPOWERED]" if p > 0.05 and "track" in status else ""
        print(
            f"{r['name']:<28}"
            f"{r['baseline']:>10.3f}"
            f"{r['target']:>10.3f}"
            f"{r['actual']:>10.3f}"
            f"{var:>7.1f}%"
            f"{p:>8.3f}"
            f"  {status}{underpowered}"
        )


if __name__ == "__main__":
    main()
