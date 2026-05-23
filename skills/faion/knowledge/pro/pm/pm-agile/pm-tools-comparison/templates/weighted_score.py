#!/usr/bin/env python3
"""
purpose: Reference script computing weighted totals from the scorecard.
consumes: see content/02-output-contract.xml inputs for pm-tools-comparison
produces: report
depends-on: content/01-core-rules.xml + content/02-output-contract.xml
token-budget-impact: ~200-1000 tokens when loaded as context
"""


"""Compute weighted scores for PM tool comparison from a YAML scorecard.

Usage:
    python weighted_score.py scorecard.yaml

scorecard.yaml format:
    weights:
      core_features: 30
      usability: 25
      integrations: 20
      enterprise: 15
      cost: 10
    tools:
      Linear:
        core_features: {score: 9.0}
        usability: {score: 9.0}
        integrations: {score: 9.0}
        enterprise: {score: 8.3}
        cost: {score: 7.0}
      Jira:
        core_features: {score: 9.7}
        usability: {score: 6.0}
        integrations: {score: 8.7}
        enterprise: {score: 10.0}
        cost: {score: 6.5}

Output: sorted ranking with weighted totals.
"""
import sys

import yaml

data = yaml.safe_load(open(sys.argv[1]))
weights = data["weights"]
results = []

for tool, cats in data["tools"].items():
    total = sum(cats[c]["score"] * weights[c] / 100 for c in cats if c in weights)
    results.append((total, tool))

results.sort(reverse=True)
print("Ranked results:")
for score, tool in results:
    print(f"  {tool}: {score:.2f}")
