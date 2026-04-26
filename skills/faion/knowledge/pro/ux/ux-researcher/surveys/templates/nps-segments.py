"""
nps-segments.py — Compute NPS overall and per segment.
Input: responses.csv with columns: recommend_0_10, plan (or other segment).
Output: NPS scores to stdout.

Install: pip install pandas
Run: python nps-segments.py responses.csv
"""
import sys
import pandas as pd


def nps(scores):
    """Compute NPS from a sequence of 0-10 scores. Returns None if n < 30."""
    s = pd.Series(scores).dropna()
    if len(s) < 30:
        return None
    promoters = (s >= 9).mean()
    detractors = (s <= 6).mean()
    return round((promoters - detractors) * 100, 1)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "responses.csv"
    df = pd.read_csv(path)

    score_col = "recommend_0_10"
    if score_col not in df.columns:
        print(f"Column '{score_col}' not found. Available: {list(df.columns)}")
        sys.exit(1)

    overall = nps(df[score_col])
    n = df[score_col].dropna().shape[0]
    print(f"Overall NPS (n={n}): {overall}")

    # Per-segment breakdown — change "plan" to your segment column
    seg_col = "plan"
    if seg_col in df.columns:
        for seg, g in df.groupby(seg_col):
            score = nps(g[score_col])
            label = str(score) if score is not None else "n<30"
            print(f"  {seg} (n={len(g)}): NPS = {label}")


if __name__ == "__main__":
    main()
