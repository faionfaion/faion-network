#!/usr/bin/env python3
"""validate-experiment.py — gate: verify experiment design has required fields, kill threshold, and sample size.

Input:  experiment YAML file with keys: hypothesis, method, audience,
        success_metric, success_threshold, kill_threshold, sample_n,
        duration_days, baseline_rate (optional), min_detectable_effect (optional)
Output: FAIL lines per violation, exits 1 if any found.
"""
import math
import sys
import yaml


REQUIRED = [
    "hypothesis",
    "method",
    "audience",
    "success_metric",
    "success_threshold",
    "kill_threshold",
    "sample_n",
    "duration_days",
]


def validate(path: str) -> list[str]:
    with open(path) as f:
        e = yaml.safe_load(f)

    errs: list[str] = []

    for k in REQUIRED:
        if not e.get(k):
            errs.append(f"missing required field: {k}")

    if e.get("success_threshold") == e.get("kill_threshold"):
        errs.append("kill_threshold must differ from success_threshold")

    # Rough power check for proportion tests (z-table at ~95% power, two-sided 5% alpha)
    baseline = e.get("baseline_rate")
    mde = e.get("min_detectable_effect")
    if baseline and mde:
        required_n = math.ceil(16 * baseline * (1 - baseline) / (mde ** 2))
        if e.get("sample_n", 0) < required_n:
            errs.append(
                f"sample_n {e['sample_n']} < required {required_n} "
                f"for baseline={baseline}, MDE={mde}"
            )

    if e.get("method") and "interview" in e["method"].lower():
        if e.get("sample_n", 0) < 5:
            errs.append("qualitative interviews: minimum 5 participants per segment")

    return errs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate-experiment.py <experiment.yaml>")
        sys.exit(2)

    errors = validate(sys.argv[1])
    for e in errors:
        print("FAIL:", e)
    sys.exit(1 if errors else 0)
