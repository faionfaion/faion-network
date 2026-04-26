"""
Sample size calculator per variant arm for binary conversion metric.
Input: baseline conversion rate, relative MDE, alpha, power
Output: required sample size per arm (int)

Usage:
  python sample-size.py
  # or import and call sample_size_per_arm() directly
"""
from math import ceil
from statsmodels.stats.power import NormalIndPower


def sample_size_per_arm(
    p_baseline: float,
    mde_relative: float,
    alpha: float = 0.05,
    power: float = 0.8,
) -> int:
    """
    p_baseline  : baseline conversion rate (e.g., 0.05 for 5%)
    mde_relative: minimum detectable effect as relative lift (e.g., 0.10 for 10% lift)
    alpha       : significance level (default 0.05)
    power       : desired statistical power (default 0.80)
    Returns     : required sample size per variant arm
    """
    p2 = p_baseline * (1 + mde_relative)
    p_avg = (p_baseline + p2) / 2
    effect = (p2 - p_baseline) / (p_avg * (1 - p_avg)) ** 0.5
    n = NormalIndPower().solve_power(
        effect_size=effect, alpha=alpha, power=power, ratio=1.0
    )
    return ceil(n)


if __name__ == "__main__":
    # Example: 5% baseline, detect +10% relative lift at 80% power
    n = sample_size_per_arm(p_baseline=0.05, mde_relative=0.10)
    print(f"Required sample size per arm: {n}")
    print(f"Total experiment size: {n * 2}")
