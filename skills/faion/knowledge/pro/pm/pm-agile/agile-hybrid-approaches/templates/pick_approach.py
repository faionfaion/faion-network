#!/usr/bin/env python3
"""Pick Predictive/Agile/Hybrid from a YAML decision file.

Usage:
    python pick_approach.py answers.yaml

answers.yaml format:
    requirements_clarity: P   # P | H | A
    stakeholder_availability: A
    risk_tolerance: H
    team_experience: A
    contract_type: H

Output: YAML with recommendation and per-factor scores.
"""
import sys

import yaml

FACTORS = [
    "requirements_clarity",
    "stakeholder_availability",
    "risk_tolerance",
    "team_experience",
    "contract_type",
]

ans = yaml.safe_load(open(sys.argv[1]))
score = {"P": 0, "A": 0, "H": 0}

for k in FACTORS:
    v = ans.get(k, "H")
    if v in score:
        score[v] += 1

if score["P"] >= 4:
    rec = "Predictive"
elif score["A"] >= 4:
    rec = "Agile"
else:
    rec = "Hybrid"

print(
    yaml.safe_dump(
        {"recommendation": rec, "scores": score},
        default_flow_style=False,
    )
)
