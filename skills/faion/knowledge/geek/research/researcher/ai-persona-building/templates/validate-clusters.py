# validate_clusters.py — silhouette scoring for automated persona pipelines
# Requires: pip install scikit-learn numpy pandas
# Abort threshold: silhouette < 0.25 → do NOT proceed to narrative generation.

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

ABORT_THRESHOLD = 0.25
CAUTION_THRESHOLD = 0.5


def find_optimal_k(
    X: np.ndarray,
    k_range: range = range(2, 8),
) -> dict:
    """
    Silhouette scoring across k range. Returns scores, recommended_k, best_score.
    Caller must check 'abort' flag before proceeding to persona generation.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    scores: dict[int, float] = {}
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        scores[k] = round(silhouette_score(X_scaled, labels), 3)

    best_k = max(scores, key=scores.get)
    best_score = scores[best_k]

    abort = best_score < ABORT_THRESHOLD
    warning = not abort and best_score < CAUTION_THRESHOLD

    return {
        "scores": scores,
        "recommended_k": best_k,
        "best_score": best_score,
        "abort": abort,           # True → pipeline must stop
        "warning": warning,       # True → proceed with caution
        "message": (
            f"ABORT: score {best_score} < {ABORT_THRESHOLD}. Revise features before proceeding."
            if abort else
            f"CAUTION: score {best_score} is moderate. Validate clusters manually."
            if warning else
            f"OK: strong clusters (score={best_score}, k={best_k})."
        ),
    }


# Usage in pipeline:
# result = find_optimal_k(X_array, k_range=range(2, 7))
# if result["abort"]:
#     raise RuntimeError(result["message"])
# k = result["recommended_k"]
