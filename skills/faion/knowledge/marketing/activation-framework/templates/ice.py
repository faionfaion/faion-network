"""
ice.py — ICE scoring helper for prioritizing activation experiments.

ICE = (Impact + Confidence + Ease) / 3
Each dimension is scored 1-10.
"""


def ice_score(impact: int, confidence: int, ease: int) -> float:
    """Compute ICE score. Returns a float between 1 and 10."""
    return round((impact + confidence + ease) / 3, 2)


# Example usage from an agent building an experiment backlog:
experiments = [
    {"name": "Magic-link signup",       "i": 8, "c": 7, "e": 9},
    {"name": "Sample data on first login", "i": 7, "c": 8, "e": 8},
    {"name": "Segment-based onboarding", "i": 9, "c": 5, "e": 4},
    {"name": "Add tooltip at Aha step",  "i": 6, "c": 9, "e": 9},
]

ranked = sorted(
    [{**x, "ice": ice_score(x["i"], x["c"], x["e"])} for x in experiments],
    key=lambda r: r["ice"],
    reverse=True,
)

# ranked[0] is the highest-priority experiment to run first
