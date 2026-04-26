"""
srm_check.py — Sample Ratio Mismatch chi-square check.
Usage: python -c "from srm_check import srm; print(srm([4980, 5020], [0.5, 0.5]))"
Returns: {"chi2": float, "p": float, "pass": bool}
Pass threshold: p > 0.001 (standard industry threshold).
Must be called as a hard gate before analyst-agent declares a winner.
"""
from scipy.stats import chisquare


def srm(observed: list[int], expected_split: list[float]) -> dict:
    """
    observed: actual assignment counts per arm
    expected_split: expected proportions per arm (must sum to 1.0)
    """
    total = sum(observed)
    expected = [total * s for s in expected_split]
    stat, p = chisquare(observed, expected)
    return {"chi2": round(stat, 4), "p": round(p, 6), "pass": p > 0.001}
