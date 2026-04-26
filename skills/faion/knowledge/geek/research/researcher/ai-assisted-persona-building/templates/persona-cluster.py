# persona_cluster.py — K-means clustering on behavioral CSV data
# Requires: pip install scikit-learn pandas

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def cluster_users(csv_path: str, n_clusters: int = 4) -> pd.DataFrame:
    """
    Cluster users in a behavioral CSV into n_clusters personas.
    Returns a DataFrame with cluster summary (mean feature values + user count).
    All columns must be numeric; non-numeric columns are dropped before clustering.
    """
    df = pd.read_csv(csv_path)
    features = df.select_dtypes(include="number")

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled)

    summary = df.groupby("cluster")[features.columns].mean()
    summary["user_count"] = df.groupby("cluster").size()
    summary["user_pct"] = (summary["user_count"] / len(df) * 100).round(1)

    return summary


# Usage:
# summary = cluster_users("user_events.csv", n_clusters=4)
# print(summary.to_markdown())
# → Use validate_clusters.py first to determine the right n_clusters
