"""vendor_scoring.py — weighted vendor evaluation with sensitivity check.

Usage:
  criteria = [{"name": "Price", "weight": 0.30},
              {"name": "Experience", "weight": 0.25},
              {"name": "Technical", "weight": 0.25},
              {"name": "Timeline", "weight": 0.10},
              {"name": "References", "weight": 0.10}]
  vendors = {"Agency A": {"Price": 85, "Experience": 90, "Technical": 85,
                           "Timeline": 80, "References": 90},
             "Agency B": {"Price": 90, "Experience": 80, "Technical": 85,
                           "Timeline": 90, "References": 75}}
  print(score(criteria, vendors))
"""


def score(criteria: list[dict], vendors: dict) -> dict:
    """Score vendors; check if top-2 margin is robust to ±5% weight shifts."""
    if abs(sum(c["weight"] for c in criteria) - 1.0) > 0.01:
        raise ValueError("Weights must sum to 1.0")

    scores = {}
    for vendor, ratings in vendors.items():
        scores[vendor] = round(
            sum(c["weight"] * ratings[c["name"]] for c in criteria), 3
        )

    ranked = sorted(scores.items(), key=lambda x: -x[1])
    margin = ranked[0][1] - ranked[1][1] if len(ranked) > 1 else 1.0

    # Sensitivity: shift each criterion weight by ±5%, see if winner flips
    flips = []
    for i, crit in enumerate(criteria):
        for delta in (+0.05, -0.05):
            adj = [
                dict(c, weight=c["weight"] + (delta if j == i else 0))
                for j, c in enumerate(criteria)
            ]
            total = sum(c["weight"] for c in adj)
            adj = [dict(c, weight=c["weight"] / total) for c in adj]
            adj_scores = {
                v: sum(c["weight"] * r[c["name"]] for c in adj)
                for v, r in vendors.items()
            }
            adj_winner = max(adj_scores, key=adj_scores.__getitem__)
            if adj_winner != ranked[0][0]:
                flips.append(f"{crit['name']} {delta:+.0%}")

    return {
        "scores": scores,
        "winner": ranked[0][0],
        "margin": round(margin, 3),
        "robust": len(flips) == 0,
        "sensitivity_flips": flips,
    }
