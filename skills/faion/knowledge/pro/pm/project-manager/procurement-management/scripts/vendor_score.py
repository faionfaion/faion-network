#!/usr/bin/env python3
"""vendor_score.py — weighted vendor scoring with sensitivity analysis.

Input JSON:
{
  "weights": {"technical": 0.25, "experience": 0.20, "price": 0.25,
              "timeline": 0.15, "team": 0.10, "references": 0.05},
  "proposals": [
    {"vendor": "Agency A", "scores": {"technical": 4, "experience": 5,
     "price": 3, "timeline": 4, "team": 4, "references": 5}},
    ...
  ]
}

Output: ranked list + sensitivity analysis (rank change under ±10% weight shift).
"""
from __future__ import annotations
import json
import sys


def score(proposals: list, weights: dict) -> list:
    out = []
    for p in proposals:
        total = sum(weights[k] * p["scores"][k] for k in weights)
        out.append({"vendor": p["vendor"], "score": round(total, 2)})
    return sorted(out, key=lambda x: -x["score"])


def sensitivity(proposals: list, weights: dict, delta: float = 0.1) -> list:
    """Re-score with each weight shifted ±delta; flag rank changes."""
    results = []
    for k in weights:
        for d in (-delta, delta):
            w2 = dict(weights)
            w2[k] = max(0.0, w2[k] + d)
            total = sum(w2.values())
            w2 = {kk: vv / total for kk, vv in w2.items()}
            ranked = score(proposals, w2)
            results.append(
                {"criterion": k, "shift": d, "top_vendor": ranked[0]["vendor"]}
            )
    return results


def main(path: str) -> None:
    data = json.loads(open(path).read())
    base = score(data["proposals"], data["weights"])
    print("Ranking:", json.dumps(base, indent=2))
    sens = sensitivity(data["proposals"], data["weights"])
    rank_changes = [r for r in sens if r["top_vendor"] != base[0]["vendor"]]
    if rank_changes:
        print("\nWARNING: rank changes under sensitivity shift:")
        print(json.dumps(rank_changes, indent=2))
    else:
        print("\nRank stable under ±10% weight shifts.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: vendor_score.py <proposals.json>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
