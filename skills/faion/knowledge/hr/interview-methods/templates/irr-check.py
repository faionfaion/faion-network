#!/usr/bin/env python3
"""
irr-check.py — Inter-rater reliability check for interview scorecards.
Computes Cohen's kappa per competency across all interviewers.
Gates debrief: PASS if kappa >= 0.4 on all competencies, else RECALIBRATE.

Input (stdin): JSON object
  { "interviewer_name": { "competency_name": score_int_1_to_5 }, ... }

Output (stdout): JSON
  { "kappa_per_competency": { "comp_name": kappa_float }, "gate": "PASS|RECALIBRATE" }

Usage:
  python3 irr-check.py < scorecards.json
  echo '{"Alice":{"ownership":4,"collaboration":3},"Bob":{"ownership":3,"collaboration":4}}' | python3 irr-check.py
"""
import sys
import json
from itertools import combinations


def linear_kappa(ratings_a: list, ratings_b: list, labels: list) -> float:
    """Cohen's kappa with linear weights for ordinal scales."""
    n = len(ratings_a)
    if n == 0:
        return 0.0

    # Agreement matrix
    k = len(labels)
    label_idx = {v: i for i, v in enumerate(labels)}
    obs = [[0] * k for _ in range(k)]
    for a, b in zip(ratings_a, ratings_b):
        obs[label_idx[a]][label_idx[b]] += 1

    # Weights (linear)
    w = [[1 - abs(i - j) / (k - 1) for j in range(k)] for i in range(k)]

    # Row/col marginals
    row_marg = [sum(obs[i]) / n for i in range(k)]
    col_marg = [sum(obs[i][j] for i in range(k)) / n for j in range(k)]

    po = sum(w[i][j] * obs[i][j] / n for i in range(k) for j in range(k))
    pe = sum(w[i][j] * row_marg[i] * col_marg[j] for i in range(k) for j in range(k))

    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def kappa_matrix(scores: dict) -> dict:
    interviewers = list(scores)
    if not interviewers:
        return {}
    competencies = list(next(iter(scores.values())))
    labels = [1, 2, 3, 4, 5]
    result = {}
    for comp in competencies:
        pairs = list(combinations(interviewers, 2))
        if not pairs:
            result[comp] = None
            continue
        kappas = []
        for a, b in pairs:
            ra = [scores[a].get(comp)]
            rb = [scores[b].get(comp)]
            if ra[0] is not None and rb[0] is not None:
                kappas.append(linear_kappa(ra, rb, labels))
        result[comp] = round(sum(kappas) / len(kappas), 2) if kappas else None
    return result


if __name__ == "__main__":
    data = json.load(sys.stdin)
    kappas = kappa_matrix(data)
    gate = "PASS" if all((v or 0) >= 0.4 for v in kappas.values()) else "RECALIBRATE"
    output = {"kappa_per_competency": kappas, "gate": gate}
    json.dump(output, sys.stdout, indent=2)
    print()
    if gate == "RECALIBRATE":
        low = [c for c, v in kappas.items() if (v or 0) < 0.4]
        print(f"RECALIBRATE before debrief. Low-agreement competencies: {low}", file=sys.stderr)
        sys.exit(1)
