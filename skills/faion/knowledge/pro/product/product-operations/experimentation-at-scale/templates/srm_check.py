#!/usr/bin/env python3
# purpose: Sample Ratio Mismatch chi-square check
# consumes: CLI args: --control-n --treatment-n --expected-ratio (default 0.5)
# produces: exit 0 if SRM passes (p>=0.001); exit 1 otherwise
# depends-on: stdlib
# token-budget-impact: low

import argparse, math, sys

def chi2_p(c, t, ratio):
    n = c + t
    exp_c = n * ratio
    exp_t = n * (1 - ratio)
    chi2 = (c - exp_c) ** 2 / exp_c + (t - exp_t) ** 2 / exp_t
    # 1 dof, survival function via series approx
    # Use Q-function approx for chi2(1) which equals 2 * Phi(-sqrt(chi2))
    z = math.sqrt(chi2)
    p = math.erfc(z / math.sqrt(2))
    return chi2, p

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--control-n", type=int, required=False)
    p.add_argument("--treatment-n", type=int, required=False)
    p.add_argument("--expected-ratio", type=float, default=0.5)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        chi2, pv = chi2_p(5000, 5000, 0.5)
        ok = pv > 0.001
        sys.stdout.write(f"self-test chi2={chi2:.3f} p={pv:.4f} pass={ok}\n")
        sys.exit(0 if ok else 1)
    if a.control_n is None or a.treatment_n is None:
        sys.stderr.write("--control-n and --treatment-n required\n"); sys.exit(2)
    chi2, pv = chi2_p(a.control_n, a.treatment_n, a.expected_ratio)
    if pv < 0.001:
        sys.stderr.write(f"SRM FAIL chi2={chi2:.3f} p={pv:.4f}\n"); sys.exit(1)
    sys.stdout.write(f"SRM ok chi2={chi2:.3f} p={pv:.4f}\n")

if __name__ == "__main__":
    main()
