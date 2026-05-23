#!/usr/bin/env python3
# purpose: Compute sample size for given baseline / MDE / alpha / power
# consumes: CLI args: --baseline --mde --alpha --power
# produces: stdout: per-arm sample size
# depends-on: stdlib (math)
# token-budget-impact: low

import argparse, math, sys

def z(p):
    # cheap inverse-normal for common levels
    table = {0.5: 0.0, 0.6: 0.2533, 0.7: 0.5244, 0.8: 0.8416, 0.9: 1.2816, 0.95: 1.6449, 0.975: 1.96, 0.99: 2.3263}
    if p in table: return table[p]
    # crude linear fallback
    keys = sorted(table)
    for i in range(len(keys)-1):
        if keys[i] <= p <= keys[i+1]:
            a, b = keys[i], keys[i+1]
            return table[a] + (p - a) * (table[b] - table[a]) / (b - a)
    return table[0.975]

def size(baseline, mde, alpha, power):
    p1, p2 = baseline, baseline + mde
    pbar = (p1 + p2) / 2
    za = z(1 - alpha / 2)
    zb = z(power)
    num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1*(1-p1) + p2*(1-p2))) ** 2
    return math.ceil(num / (mde ** 2))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--baseline", type=float, default=0.1)
    p.add_argument("--mde", type=float, default=0.02)
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--power", type=float, default=0.8)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        n = size(0.1, 0.02, 0.05, 0.8)
        sys.stdout.write(f"self-test n={n}\n")
        sys.exit(0 if n > 100 else 1)
    n = size(a.baseline, a.mde, a.alpha, a.power)
    sys.stdout.write(f"per-arm sample size: {n}\n")

if __name__ == "__main__":
    main()
