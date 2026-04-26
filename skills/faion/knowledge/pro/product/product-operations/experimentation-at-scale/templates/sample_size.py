"""
sample_size.py — two-proportion z-test sample size and runtime calculator.
Usage: echo '{"baseline": 0.05, "mde_rel": 0.1, "alpha": 0.05, "power": 0.8, "daily_traffic": 5000, "split": 0.5}' | python sample_size.py
Output: {"n_per_arm": <int>, "runtime_days": <int>}
"""
import math
from statsmodels.stats.power import NormalIndPower


def required_n(baseline: float, mde_rel: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Two-proportion z-test sample size per arm."""
    p1 = baseline
    p2 = baseline * (1 + mde_rel)
    pooled = (p1 + p2) / 2
    es = (p2 - p1) / math.sqrt(pooled * (1 - pooled))
    n = NormalIndPower().solve_power(effect_size=es, alpha=alpha, power=power)
    return int(math.ceil(n))


def runtime_days(n_per_arm: int, daily_traffic: int, split: float = 0.5) -> int:
    return math.ceil(n_per_arm / (daily_traffic * split))


if __name__ == "__main__":
    import json
    import sys

    cfg = json.load(sys.stdin)
    n = required_n(cfg["baseline"], cfg["mde_rel"], cfg.get("alpha", 0.05), cfg.get("power", 0.8))
    days = runtime_days(n, cfg["daily_traffic"], cfg.get("split", 0.5))
    json.dump({"n_per_arm": n, "runtime_days": days}, sys.stdout)
