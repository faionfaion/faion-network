# segment.py — k-means clustering on usage features, emits segments.json
# Input: usage.csv with columns: customer_id, mrr, dau_w, feat_score, seats
# Output: segments.json with cluster profiles and feature importance
# Usage: python segment.py
# Requires: pip install pandas scikit-learn

import json

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("usage.csv")
features = ["mrr", "dau_w", "feat_score", "seats"]

# Standardise before clustering to prevent high-variance features dominating
X = StandardScaler().fit_transform(df[features])

# Deterministic seed for reproducibility across runs
km = KMeans(n_clusters=4, n_init=20, random_state=42).fit(X)
df["segment"] = km.labels_

profile = (
    df.groupby("segment")[features]
    .agg(["mean", "median", "count"])
    .round(2)
    .to_dict()
)

out = {
    "n_segments": 4,
    # Feature importance = variance across cluster centres (higher = more differentiating)
    "feature_importance": dict(
        zip(features, km.cluster_centers_.var(axis=0).round(4).tolist())
    ),
    "profile": profile,
    "note": (
        "Validate k with a scree plot before accepting. "
        "Check for outlier whales driving cluster 0 or 3."
    ),
}

with open("segments.json", "w") as f:
    json.dump(out, f, indent=2)

print(f"Segments written to segments.json")
print(f"Feature importance: {out['feature_importance']}")
