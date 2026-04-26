#!/usr/bin/env python3
"""ab_stats.py — A/B test sample size and significance calculator.

Usage:
    python3 ab_stats.py
    # Or import and call sample_size() / significance() directly.

Requires: scipy, statsmodels
    pip install scipy statsmodels
"""
from scipy import stats
from statsmodels.stats.power import NormalIndPower
import math


def sample_size(baseline_rate: float, mde: float, power: float = 0.8, alpha: float = 0.05) -> int:
    """Calculate required sample size per variant.

    Args:
        baseline_rate: Current conversion rate (e.g., 0.05 for 5%)
        mde: Minimum detectable effect as absolute change (e.g., 0.01 for +1pp)
        power: Statistical power (default 0.8)
        alpha: Significance level (default 0.05 = 95% confidence)

    Returns:
        Required n per variant (rounded up).
    """
    effect_size = mde / math.sqrt(baseline_rate * (1 - baseline_rate))
    analysis = NormalIndPower()
    n = analysis.solve_power(effect_size=effect_size, power=power, alpha=alpha)
    return math.ceil(n)


def significance(conv_a: int, n_a: int, conv_b: int, n_b: int) -> dict:
    """Chi-squared test for two conversion proportions.

    Args:
        conv_a: Conversions in control group
        n_a: Total users in control group
        conv_b: Conversions in variant group
        n_b: Total users in variant group

    Returns:
        dict with p_value, lift_pct (relative lift), and significant (bool).
    """
    table = [[conv_a, n_a - conv_a], [conv_b, n_b - conv_b]]
    _, p, _, _ = stats.chi2_contingency(table)
    rate_a = conv_a / n_a
    rate_b = conv_b / n_b
    lift = (rate_b - rate_a) / rate_a * 100
    return {"p_value": round(p, 4), "lift_pct": round(lift, 2), "significant": p < 0.05}


if __name__ == "__main__":
    # Example: baseline 5%, detect 1pp absolute improvement
    n = sample_size(baseline_rate=0.05, mde=0.01)
    print(f"Required n per variant: {n}")
    result = significance(conv_a=150, n_a=3000, conv_b=180, n_b=3000)
    print(f"Significance result: {result}")
