#!/usr/bin/env python3
"""Score a project against three delivery modes and recommend one.

Input JSON:
  {
    "requirement_clarity":    1-5,  # 1=evolving, 5=stable
    "stakeholder_engagement": 1-5,  # 1=limited, 5=highly engaged
    "risk_tolerance":         1-5,  # 1=low, 5=high
    "team_agility":           1-5,  # 1=less experienced, 5=self-organising
    "contract_flexibility":   1-5,  # 1=fixed-price/scope, 5=T&M
    "regulatory_burden":      1-5   # 1=low, 5=high (SOX/FDA/DoD)
  }

Usage: approach-score.py <context.json>
"""
import json
import sys

# Weights: positive = favours that mode, negative = disfavours
WEIGHTS: dict[str, dict[str, float]] = {
    "requirement_clarity":    {"predictive": +1, "agile": -1, "hybrid":  0},
    "stakeholder_engagement": {"predictive": -1, "agile": +1, "hybrid":  0},
    "risk_tolerance":         {"predictive": -1, "agile": +1, "hybrid":  0},
    "team_agility":           {"predictive": -1, "agile": +1, "hybrid":  0},
    "contract_flexibility":   {"predictive": -1, "agile": +1, "hybrid": +0.5},
    "regulatory_burden":      {"predictive": +1, "agile": -1, "hybrid": +0.5},
}


def score(ctx: dict) -> dict[str, float]:
    out: dict[str, float] = {"predictive": 0.0, "agile": 0.0, "hybrid": 0.0}
    for axis, val in ctx.items():
        if axis not in WEIGHTS:
            continue
        normalised = (val - 3) / 2  # map 1-5 → -1..+1
        for mode, weight in WEIGHTS[axis].items():
            out[mode] += normalised * weight
    return out


def recommend(ctx: dict) -> dict:
    scores = score(ctx)
    pick = max(scores, key=lambda k: scores[k])
    risks = []
    if pick == "agile" and ctx.get("contract_flexibility", 3) <= 2:
        risks.append("Fixed-price contract + agile requires a scope-envelope clause; "
                     "without it, every backlog refinement risks a contract dispute.")
    if pick in ("agile", "hybrid") and ctx.get("regulatory_burden", 1) >= 4:
        risks.append("High regulatory burden: pure agile is incompatible with mandated phase gates. "
                     "Use predictive-governance-over-agile-execution pattern.")
    return {
        "scores": {k: round(v, 2) for k, v in scores.items()},
        "recommendation": pick,
        "risks_of_recommendation": risks,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: approach-score.py <context.json>")
        sys.exit(2)
    ctx = json.load(open(sys.argv[1]))
    print(json.dumps(recommend(ctx), indent=2))
