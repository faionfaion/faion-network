"""__faion_header__
purpose: Parse Twitter Analytics CSV for engagement-rate ranking.
consumes: Twitter native CSV export with impressions + engagements columns
produces: JSON list of top tweets with engagement rate
depends-on: AGENTS.md Task Routing (score_outliers → haiku)
token-budget-impact: ~300 tokens
"""

"""
Parse Twitter Analytics CSV export for engagement rate analysis.
Expects columns: 'impressions', 'engagements', 'Tweet text' (Twitter native export format).
Filters posts with fewer than 100 impressions to remove noise.

Usage:
  python twitter-analytics.py twitter_analytics.csv
"""
import csv
import statistics
import sys


def twitter_analysis(csv_path: str) -> dict:
    """
    Returns avg engagement rate, top 5 hook patterns (first 60 chars),
    and post count analyzed.
    """
    rows: list[tuple[float, str]] = []
    rates: list[float] = []

    with open(csv_path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            imp = int(row.get("impressions", 0) or 0)
            eng = int(row.get("engagements", 0) or 0)
            text = row.get("Tweet text", "")[:60]
            if imp > 100:
                rate = eng / imp * 100
                rates.append(rate)
                rows.append((rate, text))

    rows.sort(reverse=True)
    return {
        "avg_engagement_rate": round(statistics.mean(rates), 2) if rates else 0,
        "top_5_hooks": [r[1] for r in rows[:5]],
        "posts_analyzed": len(rates),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python twitter-analytics.py <csv_path>")
        sys.exit(1)
    result = twitter_analysis(sys.argv[1])
    print(f"Posts analyzed: {result['posts_analyzed']}")
    print(f"Avg engagement rate: {result['avg_engagement_rate']}%")
    print("Top 5 hooks:")
    for i, hook in enumerate(result["top_5_hooks"], 1):
        print(f"  {i}. {hook}")
