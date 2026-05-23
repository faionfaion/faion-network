#!/usr/bin/env python3
# purpose: Bayesian belief-update tracker for product hypotheses
# consumes: CLI args: --prior --likelihood-positive --observed (1/0)
# produces: stdout: posterior belief
# depends-on: stdlib
# token-budget-impact: low

import argparse, sys

def update(prior, lik_pos, observed):
    # P(H|E) = P(E|H) P(H) / P(E); P(E) = P(E|H)P(H) + P(E|~H)P(~H)
    lik_neg = 1 - lik_pos
    if observed:
        pe = lik_pos * prior + lik_neg * (1 - prior)
        return (lik_pos * prior) / pe
    pe = lik_neg * prior + lik_pos * (1 - prior)
    return (lik_neg * prior) / pe

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prior", type=float, default=0.5)
    p.add_argument("--likelihood-positive", type=float, default=0.7)
    p.add_argument("--observed", type=int, default=1)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        post = update(0.5, 0.8, 1)
        ok = 0.7 < post < 0.85
        sys.stdout.write(f"self-test post={post:.3f} pass={ok}\n")
        sys.exit(0 if ok else 1)
    post = update(a.prior, a.likelihood_positive, a.observed)
    sys.stdout.write(f"posterior: {post:.3f}\n")

if __name__ == "__main__":
    main()
