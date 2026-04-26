#!/usr/bin/env python3
"""Risk-driven contingency via Monte Carlo over Bernoulli risk events.

Input YAML: risks list with name, probability (0-1 float), cost_impact_usd (int).
Output: expected value, P50, P80, P95 contingency amounts.
"""
import sys
import random
import yaml

N_SIMULATIONS = 10_000


def risk_contingency(risks, seed=42):
    random.seed(seed)
    expected = sum(r["probability"] * r["cost_impact_usd"] for r in risks)
    sims = []
    for _ in range(N_SIMULATIONS):
        total = sum(
            r["cost_impact_usd"]
            for r in risks
            if random.random() < r["probability"]
        )
        sims.append(total)
    sims.sort()
    return {
        "expected": round(expected),
        "p50": sims[N_SIMULATIONS // 2],
        "p80": sims[int(N_SIMULATIONS * 0.80)],
        "p95": sims[int(N_SIMULATIONS * 0.95)],
    }


def main(path):
    data = yaml.safe_load(open(path))
    risks = data["risks"]
    if not risks:
        sys.exit("ERROR: no risks in input — fix risk register before estimating contingency")
    result = risk_contingency(risks)
    print(f"Risk-driven contingency ({len(risks)} risks, {N_SIMULATIONS} simulations):")
    print(f"  Expected (EV):   ${result['expected']:,}")
    print(f"  P50:             ${result['p50']:,}")
    print(f"  P80 (baseline):  ${result['p80']:,}  <-- use this")
    print(f"  P95:             ${result['p95']:,}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: risk-contingency.py risks.yaml")
    main(sys.argv[1])
