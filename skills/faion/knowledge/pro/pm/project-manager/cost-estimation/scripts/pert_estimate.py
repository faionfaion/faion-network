#!/usr/bin/env python3
"""pert_estimate.py — PERT 3-point cost estimation from WBS JSON.

Input JSON format:
[
  {"id": "WP-01", "name": "...", "role": "dev",
   "o_h": 20, "m_h": 40, "p_h": 80, "rate_usd": 100, "rate_source": "rate-card-v2"}
]

Output: per-item PERT mean/std + project totals at P50/P80/P95.
"""
from __future__ import annotations
import json
import math
import sys


def pert(o: float, m: float, p: float) -> tuple[float, float]:
    mean = (o + 4 * m + p) / 6
    std = (p - o) / 6
    return mean, std


def check_pessimism_ratio(m: float, p: float, item_id: str) -> None:
    if m > 0 and (p / m) < 1.8:
        print(
            f"WARNING {item_id}: p/m ratio={p/m:.2f} < 1.8 — pessimistic likely underestimated",
            file=sys.stderr,
        )


def main(path: str) -> None:
    wbs: list[dict] = json.loads(open(path).read())
    total_mean = total_var = 0.0
    items = []
    for wp in wbs:
        if not wp.get("rate_source"):
            print(f"ERROR {wp['id']}: missing rate_source — reject", file=sys.stderr)
            sys.exit(1)
        check_pessimism_ratio(wp["m_h"], wp["p_h"], wp["id"])
        mh, sh = pert(wp["o_h"], wp["m_h"], wp["p_h"])
        cost_mean = mh * wp["rate_usd"]
        cost_std = sh * wp["rate_usd"]
        total_mean += cost_mean
        total_var += cost_std**2
        items.append(
            {
                "id": wp["id"],
                "name": wp.get("name", ""),
                "cost_mean_usd": round(cost_mean),
                "cost_std_usd": round(cost_std),
            }
        )
    total_std = math.sqrt(total_var)
    result = {
        "items": items,
        "total_mean_usd": round(total_mean),
        "total_std_usd": round(total_std),
        "p50_usd": round(total_mean),
        "p80_usd": round(total_mean + 0.84 * total_std),
        "p95_usd": round(total_mean + 1.65 * total_std),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: pert_estimate.py <wbs.json>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
