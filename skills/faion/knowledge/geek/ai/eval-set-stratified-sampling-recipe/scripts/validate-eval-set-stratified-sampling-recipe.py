#!/usr/bin/env python3
"""validate-eval-set-stratified-sampling-recipe.py — validate a recipe JSON.

Usage:
    validate-eval-set-stratified-sampling-recipe.py --recipe file.json
    validate-eval-set-stratified-sampling-recipe.py --self-test

Exit codes: 0=pass, 1=fail (violations printed), 2=bad invocation.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def validate(data: dict) -> list[dict]:
    v: list[dict] = []
    required = ["version", "parent_version", "created_at", "N_daily", "seed",
                "tail_floor", "head_cap_share", "strata", "drift_policy"]
    for k in required:
        if k not in data:
            v.append({"rule": "schema", "message": f"missing field: {k}"})
    if v:
        return v
    if not isinstance(data["version"], str) or not SEMVER.match(data["version"]):
        v.append({"rule": "rule:r5", "message": "version not semver"})
    n = data["N_daily"]
    if not isinstance(n, int) or n < 10:
        v.append({"rule": "schema", "message": f"N_daily invalid: {n}"})
    seed = data["seed"]
    if not isinstance(seed, int):
        v.append({"rule": "rule:r2", "message": "seed not integer"})
    tail_floor = data["tail_floor"]
    head_cap_share = data["head_cap_share"]
    strata = data["strata"]
    if not isinstance(strata, list) or len(strata) < 2:
        v.append({"rule": "schema", "message": "strata must be list len>=2"})
        return v
    total = 0
    head_cap_q = int(n * head_cap_share)
    for s in strata:
        q = s.get("quota", 0)
        total += q
        if q < tail_floor:
            v.append({"rule": "rule:r1", "message": f"stratum {s.get('key')} quota {q} < tail_floor {tail_floor}"})
        if q > head_cap_q:
            v.append({"rule": "rule:r3", "message": f"stratum {s.get('key')} quota {q} > head_cap {head_cap_q}"})
    if total != n:
        v.append({"rule": "rule:r6", "message": f"sum(quota)={total} != N_daily={n}"})
    return v


def self_test() -> int:
    good = {
        "version": "1.0.0", "parent_version": None, "created_at": "2026-05-22T07:00:00Z",
        "N_daily": 200, "seed": 42, "tail_floor": 5, "head_cap_share": 0.4,
        "drift_policy": {"abs_share_threshold": 0.1, "max_age_days": 30},
        "strata": [
            {"key": "a", "traffic_share": 0.55, "quota": 80},
            {"key": "b", "traffic_share": 0.20, "quota": 50},
            {"key": "c", "traffic_share": 0.15, "quota": 40},
            {"key": "d", "traffic_share": 0.10, "quota": 30},
        ],
    }
    assert validate(good) == [], validate(good)
    bad = dict(good, strata=[
        {"key": "head", "traffic_share": 0.92, "quota": 184},
        {"key": "tail-a", "traffic_share": 0.05, "quota": 0},
        {"key": "tail-b", "traffic_share": 0.03, "quota": 16},
    ])
    out = validate(bad)
    assert any(x["rule"] == "rule:r1" for x in out), out
    assert any(x["rule"] == "rule:r3" for x in out), out
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--recipe", type=Path, help="Path to recipe JSON file.")
    ap.add_argument("--self-test", action="store_true", help="Run built-in fixture; exit 0 on pass.")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.recipe:
        ap.error("--recipe required (or --self-test)")
        return 2
    data = json.loads(args.recipe.read_text(encoding="utf-8"))
    out = validate(data)
    sys.stdout.write(json.dumps({"ok": not out, "violations": out}, indent=2) + "\n")
    return 0 if not out else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
