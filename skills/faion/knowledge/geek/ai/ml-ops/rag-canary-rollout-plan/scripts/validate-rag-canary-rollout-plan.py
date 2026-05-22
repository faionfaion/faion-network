#!/usr/bin/env python3
"""Validate output contract for rag-canary-rollout-plan.

USAGE:
    validate-rag-canary-rollout-plan.py <input.json>   Validate a rollout plan.
    validate-rag-canary-rollout-plan.py --self-test    Run built-in fixture.
    validate-rag-canary-rollout-plan.py --help         Show this help.

EXIT CODES:
    0 on pass
    1 on schema violation
    2 on usage error

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXPECTED_PERCENTS = [1, 5, 25, 100]
EXPECTED_HOLD_MIN = {1: 24, 5: 24, 25: 48, 100: 168}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("feature_id", "target_version", "baseline_version", "steps", "golden_eval", "online_quality", "kill_switch"):
        if k not in c:
            v.append(f"missing required field: {k}")
    if c.get("target_version") == c.get("baseline_version"):
        v.append("target_version must differ from baseline_version")
    steps = c.get("steps") or []
    if not isinstance(steps, list) or len(steps) != 4:
        v.append("steps must have exactly 4 entries (rule r1)")
    if isinstance(steps, list):
        for i, s in enumerate(steps):
            if not isinstance(s, dict):
                v.append(f"steps[{i}] must be object")
                continue
            pct = s.get("percent")
            if i < len(EXPECTED_PERCENTS) and pct != EXPECTED_PERCENTS[i]:
                v.append(f"steps[{i}].percent must be {EXPECTED_PERCENTS[i]} (rule r1)")
            hold = s.get("hold_hours", 0)
            if pct in EXPECTED_HOLD_MIN and hold < EXPECTED_HOLD_MIN[pct]:
                v.append(f"steps[{i}].hold_hours {hold} < required {EXPECTED_HOLD_MIN[pct]} (rule r1)")
    ge = c.get("golden_eval") or {}
    thr = ge.get("thresholds") or {}
    if thr.get("primary_no_regression") is not True:
        v.append("golden_eval.thresholds.primary_no_regression must be true (rule r2)")
    if isinstance(thr.get("secondary_max_regression_pct"), (int, float)) and thr["secondary_max_regression_pct"] > 5:
        v.append("golden_eval.thresholds.secondary_max_regression_pct must be <=5 (rule r2)")
    if isinstance(thr.get("p95_latency_max_delta_pct"), (int, float)) and thr["p95_latency_max_delta_pct"] > 20:
        v.append("golden_eval.thresholds.p95_latency_max_delta_pct must be <=20 (rule r2)")
    oq = c.get("online_quality") or {}
    sr = oq.get("sample_rate")
    if isinstance(sr, (int, float)) and sr < 0.05:
        v.append(f"online_quality.sample_rate {sr} < 0.05 — too thin (rule r3, fm-02)")
    ks = c.get("kill_switch") or {}
    if ks.get("atomic_flip") is not True:
        v.append("kill_switch.atomic_flip must be true (rule r4)")
    if len(ks.get("criteria") or []) < 4:
        v.append("kill_switch.criteria must have >=4 entries (rule r4)")
    rwd = ks.get("rehearsed_within_days")
    if isinstance(rwd, int) and rwd > 90:
        v.append("kill_switch.rehearsed_within_days must be <=90")
    return v


def _self_test() -> int:
    good = {
        "feature_id": "support-bot-rag-v3",
        "target_version": "v3",
        "baseline_version": "v2",
        "steps": [
            {"percent": 1, "hold_hours": 24, "min_samples": 200},
            {"percent": 5, "hold_hours": 24, "min_samples": 1000},
            {"percent": 25, "hold_hours": 48, "min_samples": 5000},
            {"percent": 100, "hold_hours": 168, "min_samples": 10000},
        ],
        "golden_eval": {
            "suite_id": "gold-v3",
            "thresholds": {"primary_no_regression": True, "secondary_max_regression_pct": 3, "p95_latency_max_delta_pct": 15},
        },
        "online_quality": {"rubric_id": "rubric-v1", "sample_rate": 0.08, "floor_composite_score": 0.8},
        "kill_switch": {"criteria": ["score_drop_5pp", "p95_latency_doubled", "error_rate_5pct", "hallucination_spike"],
                         "atomic_flip": True, "rehearsed_within_days": 30},
    }
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = dict(good); bad["online_quality"] = {**good["online_quality"], "sample_rate": 0.01}
    assert any("sample_rate" in x for x in validate(bad)), "should flag thin sampling"
    bad = dict(good); bad["kill_switch"] = {**good["kill_switch"], "atomic_flip": False}
    assert any("atomic_flip" in x for x in validate(bad)), "should flag non-atomic flip"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-rag-canary-rollout-plan.py")
    p.add_argument("path", nargs="?", help="JSON plan to validate")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
