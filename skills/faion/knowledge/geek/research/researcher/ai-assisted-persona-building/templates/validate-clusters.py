# validate_clusters.py — silhouette scoring to find optimal k
# Requires: pip install scikit-learn numpy pandas
# Silhouette score interpretation:
#   > 0.5  → strong clusters; proceed
#   0.25-0.5 → moderate; proceed with caution
#   < 0.25 → weak; revise feature selection before building personas

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def find_optimal_k(
    csv_path: str,
    k_range: range = range(2, 8),
) -> dict:
    """
    Run K-means for each k in k_range. Return silhouette scores and recommended k.
    Aborts with a warning if best silhouette < 0.25 — do not proceed to persona generation.
    """
    df = pd.read_csv(csv_path)
    X = df.select_dtypes(include="number").values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    scores: dict[int, float] = {}
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        scores[k] = round(silhouette_score(X_scaled, labels), 3)

    best_k = max(scores, key=scores.get)
    best_score = scores[best_k]

    if best_score < 0.25:
        print(f"WARNING: Best silhouette score {best_score} < 0.25. "
              "Clusters are weak — revise feature selection before building personas.")
    elif best_score < 0.5:
        print(f"NOTE: Silhouette score {best_score} is moderate. Proceed with caution.")
    else:
        print(f"OK: Strong clusters detected (score={best_score}, k={best_k}).")

    return {"scores": scores, "recommended_k": best_k, "best_score": best_score}


# Usage:
# result = find_optimal_k("user_events.csv", k_range=range(2, 7))
# print(result)
