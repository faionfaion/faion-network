#!/usr/bin/env python3
"""
segment-candidates.py — emit candidate behavioral clusters from a user CSV.

Usage: python segment-candidates.py users.csv [k_max] > candidates.json

Input: CSV with numeric columns representing user behavioral features
  (e.g. login_days, features_used, support_tickets, sessions_last_30d)
Output: JSON with best k, silhouette score, and per-segment profile means

Requires: pandas, scikit-learn
Install: pip install pandas scikit-learn
"""
import json
import sys

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def main(csv_path: str, k_max: int) -> None:
    df = pd.read_csv(csv_path)
    num = df.select_dtypes(include="number").fillna(0)
    if num.shape[1] < 2:
        print("ERROR: need at least 2 numeric columns for clustering", file=sys.stderr)
        sys.exit(1)

    X = StandardScaler().fit_transform(num)

    best: dict = {"k": None, "score": -1.0, "labels": None}
    for k in range(2, min(k_max + 1, len(df))):
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        score = float(silhouette_score(X, km.labels_))
        if score > best["score"]:
            best = {"k": k, "score": score, "labels": km.labels_.tolist()}

    df["segment"] = best["labels"]
    profiles = []
    for seg_id, group in df.groupby("segment"):
        profiles.append({
            "segment_id": int(seg_id),
            "n": int(len(group)),
            "share": round(len(group) / len(df), 3),
            "means": {col: round(float(group[col].mean()), 2) for col in num.columns},
        })

    result = {
        "k": best["k"],
        "silhouette_score": round(best["score"], 4),
        "note": "These are behavioral clusters, not named personas. Human review required before naming.",
        "profiles": profiles,
    }
    print(json.dumps(result, indent=2))
    print(f"\nNext step: show profiles to human for dimension naming and evidence review.", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <users.csv> [k_max=5]", file=sys.stderr)
        sys.exit(1)
    _k_max = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    main(sys.argv[1], _k_max)
