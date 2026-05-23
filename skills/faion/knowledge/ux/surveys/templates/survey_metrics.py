"""
survey_metrics.py — Deterministic NPS and SUS calculator.

Usage:
    python survey_metrics.py responses.csv

CSV expectations:
    - Column "nps": integers 0-10 (NPS question responses)
    - Columns "sus_1" through "sus_10": integers 1-5 (SUS item responses)
      Items 1,3,5,7,9 are positive-phrased; items 2,4,6,8,10 are negative-phrased.

Run as code, NOT via LLM completion — LLMs make arithmetic errors on metric formulas.
"""
import sys
import pandas as pd


def nps(series: pd.Series) -> float:
    """Net Promoter Score. Range: -100 to +100."""
    s = series.dropna().astype(int)
    promoters = (s >= 9).mean() * 100
    detractors = (s <= 6).mean() * 100
    return round(promoters - detractors, 1)


# SUS: 10 items, alternating positive/negative phrasing, scale 1-5
SUS_POS = [0, 2, 4, 6, 8]   # 0-indexed positions of positive items
SUS_NEG = [1, 3, 5, 7, 9]   # 0-indexed positions of negative items


def sus(row: list[int]) -> float:
    """System Usability Scale score for one respondent. Range: 0-100. Average = 68."""
    pos = sum(row[i] - 1 for i in SUS_POS)
    neg = sum(5 - row[i] for i in SUS_NEG)
    return (pos + neg) * 2.5


def interpret_sus(score: float) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 68:
        return "Good (above average)"
    if score >= 50:
        return "OK (below average)"
    return "Poor"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python survey_metrics.py responses.csv")
        sys.exit(1)

    df = pd.read_csv(sys.argv[1])

    if "nps" in df.columns:
        score = nps(df["nps"])
        print(f"NPS: {score}")

    sus_cols = [c for c in df.columns if c.startswith("sus_")]
    if len(sus_cols) == 10:
        df["sus_score"] = df[sus_cols].apply(lambda r: sus(list(r)), axis=1)
        mean = round(df["sus_score"].mean(), 1)
        print(f"SUS mean: {mean} — {interpret_sus(mean)}")
    elif sus_cols:
        print(f"Warning: found {len(sus_cols)} SUS columns, expected 10. Skipping SUS.")
