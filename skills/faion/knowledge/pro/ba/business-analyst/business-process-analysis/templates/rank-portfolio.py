#!/usr/bin/env python3
"""rank-portfolio.py scorecard.csv -> ranked.csv (top automation/redesign candidates).

Ranks processes by: nva_minutes_per_year x feasibility x (1 - 0.5 x risk).
Required columns: volume_per_year, cycle_time_min, nva_pct,
                  automation_candidate_score (1-5), risk_score (1-5).

Usage: python rank-portfolio.py scorecard.csv
Output: ranked.csv (top 20 printed to stdout)
"""
import sys
import pandas as pd


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("Usage: rank-portfolio.py scorecard.csv")

    df = pd.read_csv(sys.argv[1])
    required = {"volume_per_year", "cycle_time_min", "nva_pct",
                "automation_candidate_score", "risk_score"}
    missing = required - set(df.columns)
    if missing:
        sys.exit(f"missing columns: {missing}")

    df["nva_minutes_per_year"] = (
        df["volume_per_year"] * df["cycle_time_min"] * df["nva_pct"] / 100
    )

    def norm(s: pd.Series) -> pd.Series:
        return (s - s.min()) / (s.max() - s.min() + 1e-9)

    df["impact"] = norm(df["nva_minutes_per_year"])
    df["feasibility"] = norm(df["automation_candidate_score"])
    df["risk"] = norm(df["risk_score"])
    df["score"] = df["impact"] * df["feasibility"] * (1 - 0.5 * df["risk"])

    display_cols = [
        c for c in ["pcf_l2_code", "pcf_l2_name", "owner", "decision",
                    "nva_minutes_per_year", "score"]
        if c in df.columns
    ]
    ranked = df.sort_values("score", ascending=False)[display_cols]
    ranked.to_csv("ranked.csv", index=False)
    print(ranked.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
