"""
Partnership candidate scoring — ranks candidates 0-25, flags proceed/no.

Scoring factors (each 1–5):
  reach      — size and quality of their audience
  relevance  — how closely their audience matches your ICP
  trust      — how much their audience trusts their recommendations
  effort     — how much work the partnership requires (LOWER is better)
  risk       — reputational/legal/operational risk (LOWER is better)

Score = reach + relevance + trust + (6 - effort) + (6 - risk)
Max = 5 + 5 + 5 + 5 + 5 = 25
Proceed threshold: >= 18

Input CSV columns:
  partner, reach_1_5, relevance_1_5, trust_1_5, effort_1_5, risk_1_5

Usage:
    python partner-score.py candidates.csv shortlist.csv
"""

import sys

import pandas as pd


def score(row: pd.Series) -> int:
    return (
        row["reach_1_5"]
        + row["relevance_1_5"]
        + row["trust_1_5"]
        + (6 - row["effort_1_5"])
        + (6 - row["risk_1_5"])
    )


def main(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)

    required = ["partner", "reach_1_5", "relevance_1_5", "trust_1_5", "effort_1_5", "risk_1_5"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["score"] = df.apply(score, axis=1)
    df["proceed"] = df["score"] >= 18

    result = df.sort_values("score", ascending=False)
    result.to_csv(output_path, index=False)

    proceed_count = df["proceed"].sum()
    print(f"Scored {len(df)} candidates. Proceed: {proceed_count}. Saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python partner-score.py <input.csv> <output.csv>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
