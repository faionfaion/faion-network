# purpose: legacy template for ads-ab-testing-ads — bayesian-ab
# consumes: per AGENTS.md Prerequisites
# produces: artefact per content/02-output-contract.xml
# depends-on: content/01-core-rules.xml, content/06-decision-tree.xml
# token-budget-impact: ~400-1200 tokens when loaded as context

"""
bayesian_ab.py

Bayesian Beta-binomial A/B test verdict for ad click/conversion tests.
Uses Beta(1,1) uninformative prior (equivalent to no prior knowledge).

Usage:
    result = bayesian_ab(clicks_a=150, exp_a=10000, clicks_b=200, exp_b=10000)
    # result: {"p_variant_better": 0.9812, "expected_lift": 0.33, "winner": "variant"}

Decision rule:
    p_variant_better > 0.95  → variant wins
    p_variant_better < 0.05  → control wins
    otherwise               → inconclusive (extend test)
"""

import numpy as np


def bayesian_ab(
    clicks_a: int,
    exp_a: int,
    clicks_b: int,
    exp_b: int,
    draws: int = 200_000,
) -> dict:
    """Compute Bayesian posterior for variant (B) outperforming control (A)."""
    rng = np.random.default_rng(42)
    # Conjugate Beta update: Beta(1 + successes, 1 + failures)
    a_samples = rng.beta(1 + clicks_a, 1 + exp_a - clicks_a, draws)
    b_samples = rng.beta(1 + clicks_b, 1 + exp_b - clicks_b, draws)
    p_b_better = float((b_samples > a_samples).mean())
    expected_lift = float(((b_samples - a_samples) / a_samples).mean())
    if p_b_better > 0.95:
        winner = "variant"
    elif p_b_better < 0.05:
        winner = "control"
    else:
        winner = "inconclusive"
    return {
        "p_variant_better": round(p_b_better, 4),
        "expected_lift": round(expected_lift, 4),
        "winner": winner,
    }
