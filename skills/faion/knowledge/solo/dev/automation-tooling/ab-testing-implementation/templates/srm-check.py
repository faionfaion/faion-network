"""SRM (sample-ratio mismatch) guard for A/B experiment analysis.

Fail if the observed traffic split deviates significantly from the configured
allocation. An SRM indicates a bucketing or logging bug; analysis on SRM data
produces biased lift estimates.

Usage:
    python srm_check.py '{"control": 49210, "treatment": 50790}' \
                        '{"control": 0.5, "treatment": 0.5}'
    # exits 0 if no SRM, exits 1 if SRM detected
"""
import sys
import json
from scipy.stats import chisquare


def srm_check(
    observed: dict[str, int],
    expected_split: dict[str, float],
    alpha: float = 0.001,
) -> bool:
    """
    Run chi-square SRM check.

    Args:
        observed:       {variant_name: observed_count}
        expected_split: {variant_name: configured_allocation} (must sum to 1.0)
        alpha:          Significance threshold (default 0.001 — stricter than p<0.05)

    Returns:
        True if no SRM (safe to proceed), False if SRM detected.
    """
    total = sum(observed.values())
    keys = list(observed.keys())
    obs = [observed[k] for k in keys]
    exp = [expected_split[k] * total for k in keys]

    chi2, p = chisquare(obs, f_exp=exp)
    print(f"SRM check: chi2={chi2:.3f} p={p:.4f} (threshold={alpha})")

    if p <= alpha:
        print(
            f"SRM DETECTED (p={p:.4f} <= {alpha}). "
            "Do NOT run analysis — check assignment logic and exposure logging."
        )
        return False

    print("No SRM detected. Safe to proceed with analysis.")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: srm_check.py '<observed_dict>' '<split_dict>'")
        sys.exit(2)

    observed = json.loads(sys.argv[1])
    expected_split = json.loads(sys.argv[2])
    ok = srm_check(observed, expected_split)
    sys.exit(0 if ok else 1)
