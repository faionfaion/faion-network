# purpose: sample-size calculator for A/B tests (target lift + significance + power)
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~400-1000 tokens when loaded as context

"""
sample_size.py — minimum sample per arm for a binary conversion A/B test.
Two-sided, 95% confidence, 80% power, equal allocation.

Usage:
    python sample_size.py
    # or import and call n_per_arm(baseline_rate, relative_mde)

Args:
    p1        : baseline conversion rate (e.g. 0.04 for 4%)
    mde_rel   : minimum detectable effect as relative lift (e.g. 0.10 for +10%)

Returns:
    Minimum number of observations required per variant arm.
"""
import math


def n_per_arm(p1: float, mde_rel: float) -> int:
    p2 = p1 * (1 + mde_rel)
    p_bar = (p1 + p2) / 2
    z_a, z_b = 1.96, 0.84  # 95% / 80%
    num = (
        z_a * math.sqrt(2 * p_bar * (1 - p_bar))
        + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    ) ** 2
    return math.ceil(num / (p2 - p1) ** 2)


if __name__ == "__main__":
    examples = [
        (0.04, 0.10),  # 4% baseline, +10% relative MDE
        (0.15, 0.15),  # 15% baseline, +15% relative MDE
        (0.30, 0.05),  # 30% baseline, +5% relative MDE
    ]
    print(f"{'Baseline':>10} {'MDE (rel)':>10} {'N/arm':>8}")
    for p1, mde in examples:
        print(f"{p1:>10.1%} {mde:>10.0%} {n_per_arm(p1, mde):>8,}")
