"""
stat_check.py — Two-proportion z-test + power analysis helper.

Usage:
    result = check(n1=15000, x1=450, n2=15000, x2=525)
    n = sample_size(baseline=0.05, mde_rel=0.10)
"""
import math
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.power import NormalIndPower


def check(n1: int, x1: int, n2: int, x2: int, alpha: float = 0.05) -> dict:
    """Run two-proportion z-test. Returns p, z, CI, lift, and significance flag."""
    z, p = proportions_ztest([x1, x2], [n1, n2])
    p1, p2 = x1 / n1, x2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    diff = p2 - p1
    ci = (diff - 1.96 * se, diff + 1.96 * se)
    return {
        "p_value": round(p, 4),
        "z": round(z, 3),
        "lift_abs": round(diff, 4),
        "lift_rel": round(diff / p1, 4) if p1 > 0 else None,
        "ci_95": [round(ci[0], 4), round(ci[1], 4)],
        "significant_at_alpha": p < alpha,
        "alpha": alpha,
    }


def sample_size(baseline: float, mde_rel: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """Compute required n per variant. mde_rel is the relative MDE (e.g. 0.10 = 10%)."""
    mde_abs = baseline * mde_rel
    effect = mde_abs / math.sqrt(baseline * (1 - baseline))
    return math.ceil(NormalIndPower().solve_power(
        effect_size=effect, alpha=alpha, power=power, alternative="two-sided"
    ))
