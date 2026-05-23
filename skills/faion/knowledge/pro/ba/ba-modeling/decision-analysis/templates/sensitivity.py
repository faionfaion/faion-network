#!/usr/bin/env python3
# purpose: Monte Carlo ±20% weight-jitter sensitivity over a locked matrix
# consumes: matrix JSON (options, criteria with weight, scores)
# produces: sensitivity{} block with rank_flip_rate + unstable_pairs
# depends-on: content/01-core-rules.xml r4
# token-budget-impact: 0 (runs in shell, not LLM)
"""
sensitivity.py — Monte Carlo sensitivity analysis for decision matrices.

Input JSON format:
  {"weights": {"cost": 0.25, "features": 0.25, ...},
   "scores":  {"opt_a": {"cost": 4, "features": 5, ...}, ...}}

Usage: python sensitivity.py matrix.json
Exit:  prints robustness % per option; exits 1 if top option wins < 70% of trials.
"""
import json, sys, random, statistics


def weighted_total(weights, scores):
    return sum(weights[c] * scores[c] for c in weights)


def perturb(weights, sigma=0.2):
    p = {c: max(0.01, w * random.gauss(1, sigma)) for c, w in weights.items()}
    s = sum(p.values())
    return {c: w / s for c, w in p.items()}


m = json.load(open(sys.argv[1]))
N = 2000
wins = {opt: 0 for opt in m["scores"]}
totals = {opt: [] for opt in m["scores"]}

for _ in range(N):
    w = perturb(m["weights"])
    scored = {opt: weighted_total(w, m["scores"][opt]) for opt in m["scores"]}
    winner = max(scored, key=scored.get)
    wins[winner] += 1
    for opt, t in scored.items():
        totals[opt].append(t)

print("Robustness under +/-20% weight noise (2000 Monte Carlo trials):")
ranked = sorted(wins.items(), key=lambda x: -x[1])
for opt, w in ranked:
    pct = 100 * w / N
    print(f"  {opt}: {pct:.1f}%  mean={statistics.mean(totals[opt]):.2f}  sd={statistics.stdev(totals[opt]):.2f}")

top_opt, top_wins = ranked[0]
top_pct = 100 * top_wins / N
if top_pct < 70:
    print(f"\nWARNING: '{top_opt}' wins only {top_pct:.1f}% of trials — recommendation is FRAGILE.")
    print("Escalate to human or gather more evidence before committing.")
    sys.exit(1)
else:
    print(f"\nOK: '{top_opt}' is robust ({top_pct:.1f}% > 70% threshold).")
