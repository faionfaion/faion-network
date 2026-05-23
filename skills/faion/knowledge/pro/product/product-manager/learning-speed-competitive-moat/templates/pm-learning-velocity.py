#!/usr/bin/env python3
"""
purpose: Compute decision-velocity per category; emits JSON.
consumes: input from methodology
produces: artefact for downstream agent
depends-on: content/02-output-contract.xml
token-budget-impact: 0 (executes locally)
"""

"""
pm_learning_velocity.py — score a PM's learning velocity from their decision log.
Inputs:
  decisions.yaml  (list of {id, ts, bet_id, decision, prediction, check_back_date, outcome, quarter, reversed_within_days})
Usage: python pm_learning_velocity.py decisions.yaml [--quarter 2026Q2]
"""
import sys, yaml, datetime, argparse, statistics

ap = argparse.ArgumentParser()
ap.add_argument("path")
ap.add_argument("--quarter", default=None)
args = ap.parse_args()

decisions = yaml.safe_load(open(args.path)) or []
if args.quarter:
    decisions = [d for d in decisions if d.get("quarter") == args.quarter]
if not decisions:
    sys.exit("no decisions in scope")

n = len(decisions)
reversed30 = sum(
    1 for d in decisions
    if d.get("reversed_within_days") and d["reversed_within_days"] <= 30
)
graded = [d for d in decisions if d.get("outcome") in ("hit", "miss")]
hit_rate = sum(1 for d in graded if d["outcome"] == "hit") / len(graded) if graded else None
kills = sum(1 for d in decisions if d["decision"] == "kill")
reframes = sum(1 for d in decisions if d["decision"] == "reframe")
mean_time_to_check = statistics.mean(
    [
        (
            datetime.date.fromisoformat(d["check_back_date"])
            - datetime.date.fromisoformat(d["ts"][:10])
        ).days
        for d in decisions if d.get("check_back_date")
    ]
) if decisions else 0

print(f"Decisions logged       : {n}")
print(f"Kill / reframe ratio   : {(kills + reframes) / n:.0%}  (target >=30%)")
print(f"Reversed within 30 days: {reversed30 / n:.0%}      (target <=15%)")
print(f"Mean time to check-back: {mean_time_to_check:.0f} days  (target <=21)")
if hit_rate is not None:
    print(f"Prediction hit rate    : {hit_rate:.0%}  (target 0.55-0.75 — outside = miscalibrated)")
else:
    print("Prediction hit rate    : insufficient graded sample")
