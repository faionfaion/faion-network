"""
Creator scoring for influencer marketing candidate ranking.

Input:  CSV with columns:
        handle, followers, engagement_rate, audience_country_pct_target,
        follower_spike_90d (ratio, e.g. 3.0 = 3x spike), niche_fit_0_1,
        content_quality_0_1

Output: CSV sorted by score, with suspect flag

Weights: engagement 0.40, audience match 0.30, niche fit 0.20, content quality 0.10
Disqualifiers: suspect spike (>3x in 90d) OR engagement rate < 1.5%

Usage:
    python score-creator.py candidates.csv shortlist.csv
"""

import sys

import pandas as pd


def score(row: pd.Series) -> float:
    er = row["engagement_rate"]
    spike = row["follower_spike_90d"]
    audience_match = row["audience_country_pct_target"]

    # Hard disqualifiers
    if spike > 3.0 or er < 0.015:
        return 0.0

    # Weighted score: engagement capped at 5% benchmark, others 0-1
    score_er = min(er / 0.05, 1.0) * 0.40
    score_audience = audience_match * 0.30
    score_niche = row["niche_fit_0_1"] * 0.20
    score_quality = row["content_quality_0_1"] * 0.10

    return round(score_er + score_audience + score_niche + score_quality, 3)


def main(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)

    required = ["handle", "engagement_rate", "audience_country_pct_target",
                "follower_spike_90d", "niche_fit_0_1", "content_quality_0_1"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["score"] = df.apply(score, axis=1)
    df["suspect"] = df["follower_spike_90d"] > 3.0
    df["qualified"] = df["score"] > 0

    result = df.sort_values("score", ascending=False)
    result.to_csv(output_path, index=False)
    print(f"Scored {len(df)} candidates. Qualified: {df['qualified'].sum()}. Saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python score-creator.py <input.csv> <output.csv>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
