"""
Co-occurrence matrix from open card sort export.

Input: list of session dicts, each with a 'groups' list.
Each group has a 'cards' list of card label strings.

Output: dict mapping (card_a, card_b) → co-occurrence rate (0.0 to 1.0)

Usage:
    sessions = [
        {"participant_id": "P1", "groups": [
            {"group_name": "Computers", "cards": ["Laptop", "Desktop", "Monitor"]},
            {"group_name": "Phones", "cards": ["iPhone", "Android Phone"]},
        ]},
        ...
    ]
    matrix = cooccurrence(sessions)
    strong = strong_clusters(matrix, threshold=0.7)
"""

from itertools import combinations
from collections import defaultdict


def cooccurrence(sessions: list) -> dict:
    """Compute pairwise co-occurrence rates across all participant sessions."""
    pair_count: dict = defaultdict(int)
    total = len(sessions)
    for s in sessions:
        for group in s.get("groups", []):
            cards = group.get("cards", [])
            for a, b in combinations(sorted(cards), 2):
                pair_count[(a, b)] += 1
    return {pair: count / total for pair, count in pair_count.items()}


def strong_clusters(matrix: dict, threshold: float = 0.7) -> dict:
    """Return pairs above the co-occurrence threshold."""
    return {pair: pct for pair, pct in matrix.items() if pct >= threshold}


def outlier_cards(matrix: dict, threshold: float = 0.4) -> list:
    """Return cards with no co-occurrence above threshold with any partner."""
    above_threshold = set()
    for (a, b), pct in matrix.items():
        if pct >= threshold:
            above_threshold.add(a)
            above_threshold.add(b)
    all_cards = {card for pair in matrix for card in pair}
    return sorted(all_cards - above_threshold)


def summarize(matrix: dict) -> None:
    """Print a human-readable summary of clustering results."""
    strong = strong_clusters(matrix, 0.7)
    borderline = {p: v for p, v in matrix.items() if 0.4 <= v < 0.7}
    outliers = outlier_cards(matrix, 0.4)

    print(f"Strong clusters (>70%): {len(strong)} pairs")
    for (a, b), pct in sorted(strong.items(), key=lambda x: -x[1]):
        print(f"  {pct:.0%}  {a} + {b}")

    print(f"\nBorderline (40-70%): {len(borderline)} pairs")
    for (a, b), pct in sorted(borderline.items(), key=lambda x: -x[1])[:10]:
        print(f"  {pct:.0%}  {a} + {b}")

    print(f"\nOutlier cards (investigate): {outliers}")
