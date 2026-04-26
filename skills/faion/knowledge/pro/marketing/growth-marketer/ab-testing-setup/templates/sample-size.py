# sample_size.py — accurate A/B test sample size and duration using statsmodels
# Input: baseline conversion rate, relative MDE, optional alpha/power/split/alternative
# Output: n_per_variant (int), duration_days (int)

import math
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def n_per_variant(
    baseline: float,
    mde_rel: float,
    alpha: float = 0.05,
    power: float = 0.80,
    ratio: float = 1.0,
    alternative: str = "two-sided",
) -> int:
    """
    baseline: current conversion rate, e.g. 0.10 for 10%
    mde_rel:  minimum detectable effect as relative fraction, e.g. 0.10 for +10% relative
    ratio:    n_control / n_treatment (1.0 = 50/50; 9.0 = 90/10 split)
    Returns n for the SMALLER arm.
    """
    p2 = baseline * (1 + mde_rel)
    effect = proportion_effectsize(p2, baseline)
    n = NormalIndPower().solve_power(
        effect_size=abs(effect),
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative=alternative,
    )
    return math.ceil(n)


def duration_days(
    n: int,
    daily_users: int,
    variants: int = 2,
) -> int:
    """
    n:           n_per_variant from the smaller arm
    daily_users: true daily average (including weekends); divide weekday avg by 5/7 if needed
    """
    return math.ceil((n * variants) / max(daily_users, 1))


# Example
if __name__ == "__main__":
    n = n_per_variant(baseline=0.10, mde_rel=0.10)
    days = duration_days(n, daily_users=2000)
    p2 = 0.10 * 1.10
    print(f"baseline=10%  mde_rel=10%  p2={p2:.3f}")
    print(f"n_per_variant={n}  total={n*2}  duration={days}d @ 2000 users/day")
