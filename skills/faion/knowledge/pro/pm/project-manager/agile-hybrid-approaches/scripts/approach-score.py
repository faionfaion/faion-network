#!/usr/bin/env python3
"""approach-score.py

Score 6 dimensions (Boehm + Turner home-ground model) and recommend
predictive / agile / named hybrid.

Inputs:
    --file PATH       6-dimension JSON
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = recommendation produced
    1 = invalid input
    2 = usage / unreadable

Dimensions (0..1 scale; 1 = strong agile signal):
    requirement_volatility
    team_skill_uniformity
    failure_cost_low
    team_size_small
    culture_fit_agile
    domain_uncertainty_high

Decision rule:
    avg >= 0.7 → agile
    avg <= 0.3 → predictive
    else → hybrid (with named tilt)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DIMS = [
    "requirement_volatility", "team_skill_uniformity", "failure_cost_low",
    "team_size_small", "culture_fit_agile", "domain_uncertainty_high",
]

FIXTURE_AGILE = {d: 0.9 for d in DIMS}
FIXTURE_PRED = {d: 0.1 for d in DIMS}
FIXTURE_HYBRID = {d: 0.5 for d in DIMS}


def recommend(scores: dict) -> tuple[str, float]:
    vals = [float(scores[d]) for d in DIMS]
    avg = sum(vals) / len(vals)
    if avg >= 0.7:
        return "agile", avg
    if avg <= 0.3:
        return "predictive", avg
    return "hybrid", avg


def self_test() -> int:
    if recommend(FIXTURE_AGILE)[0] != "agile":
        sys.stderr.write("self-test FAIL: agile fixture wrong\n"); return 1
    if recommend(FIXTURE_PRED)[0] != "predictive":
        sys.stderr.write("self-test FAIL: predictive fixture wrong\n"); return 1
    if recommend(FIXTURE_HYBRID)[0] != "hybrid":
        sys.stderr.write("self-test FAIL: hybrid fixture wrong\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
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
        sys.stderr.write(f"not a file: {p}\n"); return 2
    scores = json.loads(p.read_text())
    for d in DIMS:
        if d not in scores:
            sys.stderr.write(f"missing dimension: {d}\n"); return 1
    rec, avg = recommend(scores)
    sys.stdout.write(f"recommendation={rec} avg={avg:.2f}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
