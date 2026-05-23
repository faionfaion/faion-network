#!/usr/bin/env python3
# purpose: compute per-stratum quotas with proportional+floor+head-cap.
# consumes: list of (stratum_key, traffic_share), N_daily, tail_floor, head_cap_share.
# produces: list of (stratum_key, quota:int) with sum(quota) == N_daily.
# depends-on: python 3.10 stdlib.
# token-budget-impact: 0 — pure computation, runs offline.
"""Proportional-with-floor quota calculator for stratified eval sampling."""
from __future__ import annotations


def compute_quotas(
    strata: list[tuple[str, float]],
    n_daily: int,
    tail_floor: int = 5,
    head_cap_share: float = 0.4,
) -> list[tuple[str, int]]:
    if not strata or n_daily < 1:
        return []
    head_cap = int(n_daily * head_cap_share)
    raw = [(k, max(tail_floor, min(head_cap, round(n_daily * s)))) for k, s in strata]
    total = sum(q for _, q in raw)
    delta = n_daily - total
    if delta == 0:
        return raw
    # Redistribute to tail strata (sorted by share asc) one case at a time.
    order = sorted(range(len(raw)), key=lambda i: strata[i][1])
    out = [list(t) for t in raw]
    i = 0
    step = 1 if delta > 0 else -1
    while delta != 0 and order:
        idx = order[i % len(order)]
        new_q = out[idx][1] + step
        # Respect bounds.
        if new_q >= tail_floor and new_q <= head_cap:
            out[idx][1] = new_q
            delta -= step
        i += 1
        if i > len(order) * (abs(delta) + 10):
            break
    return [(k, q) for k, q in out]


if __name__ == "__main__":
    demo = [("head", 0.55), ("mid", 0.20), ("smb", 0.15), ("trial", 0.10)]
    for k, q in compute_quotas(demo, n_daily=200):
        # Documented stdout for demo only.
        import sys
        sys.stdout.write(f"{k}\t{q}\n")
