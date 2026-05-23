# purpose: Sample-size calculator per variant arm for a binary conversion metric
# consumes: baseline conversion rate + relative MDE + alpha + power
# produces: required sample size per arm (int) on stdout
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200 tokens when loaded
"""Sample-size calculator (proportions test, two-sided).

Pure stdlib implementation of the z-test for two proportions sample-size
formula. Equivalent to statsmodels.NormalIndPower.solve_power but with no
external dependency.

Usage:
    python sample-size.py                 # runs example
    python sample-size.py --self-test     # validates against known fixture
"""
from __future__ import annotations

import argparse
import math
import sys


def _phi_inv(p: float) -> float:
    """Inverse of the standard normal CDF (Beasley-Springer-Moro approx)."""
    if not (0.0 < p < 1.0):
        raise ValueError("p must be in (0, 1)")
    a = (-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00)
    b = (-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01)
    c = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00)
    d = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00)
    plow = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= phigh:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5]) * q / \
               (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q = math.sqrt(-2 * math.log(1 - p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
           ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def sample_size_per_arm(p_baseline: float, mde_relative: float,
                        alpha: float = 0.05, power: float = 0.8) -> int:
    """Return required sample size per arm for a two-sided z-test on proportions."""
    if not (0 < p_baseline < 1):
        raise ValueError("p_baseline must be in (0, 1)")
    p2 = p_baseline * (1 + mde_relative)
    if not (0 < p2 < 1):
        raise ValueError(f"effective p2={p2:.4f} out of range")
    z_alpha = _phi_inv(1 - alpha / 2)
    z_beta = _phi_inv(power)
    p_avg = (p_baseline + p2) / 2
    num = (z_alpha * math.sqrt(2 * p_avg * (1 - p_avg)) +
           z_beta * math.sqrt(p_baseline * (1 - p_baseline) + p2 * (1 - p2))) ** 2
    den = (p2 - p_baseline) ** 2
    return math.ceil(num / den)


def main() -> int:
    ap = argparse.ArgumentParser(description="Sample-size calculator")
    ap.add_argument("--p-baseline", type=float, default=0.05)
    ap.add_argument("--mde-relative", type=float, default=0.10)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--power", type=float, default=0.8)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        # known reference: p=0.05, mde=0.10, alpha=0.05, power=0.8 -> ~31000-32000/arm
        n = sample_size_per_arm(0.05, 0.10)
        if not (29000 <= n <= 36000):
            sys.stderr.write(f"self-test failed: n={n}\n")
            return 1
        sys.stdout.write(f"self-test OK (n={n})\n")
        return 0
    n = sample_size_per_arm(args.p_baseline, args.mde_relative, args.alpha, args.power)
    sys.stdout.write(f"Required sample size per arm: {n}\n")
    sys.stdout.write(f"Total experiment size: {n * 2}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
