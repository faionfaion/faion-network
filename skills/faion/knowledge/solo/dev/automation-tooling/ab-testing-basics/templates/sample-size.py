"""Sample size calculation for A/B tests using z-test for two proportions."""
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def sample_size_per_variant(
    p_control: float,
    mde_abs: float,
    alpha: float = 0.05,
    power: float = 0.8,
) -> int:
    """
    Compute required sample size per variant for a two-proportion z-test.

    Args:
        p_control: Baseline conversion rate (e.g., 0.062 for 6.2%)
        mde_abs:   Minimum detectable effect in absolute percentage points
                   (e.g., 0.005 for +0.5pp — NOT relative lift)
        alpha:     Type I error rate (default 0.05)
        power:     Statistical power (default 0.8)

    Returns:
        Minimum sample size per variant (round up).

    Example:
        >>> sample_size_per_variant(0.062, 0.005)
        # e.g., 11240 — required per variant at 80% power, alpha=0.05
    """
    effect_size = proportion_effectsize(p_control + mde_abs, p_control)
    n = NormalIndPower().solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=1.0,
        alternative="two-sided",
    )
    return int(n) + 1
