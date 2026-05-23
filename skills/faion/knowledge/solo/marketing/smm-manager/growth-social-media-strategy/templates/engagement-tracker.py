"""__faion_header__
purpose: Weekly engagement-rate tracker from platform analytics CSV.
consumes: CSV with impressions + engagements columns
produces: JSON {avg, median, top, count} engagement metrics
depends-on: AGENTS.md Task Routing (score_engagement → haiku)
token-budget-impact: ~300 tokens
"""

"""
Weekly engagement rate tracker from platform analytics CSV exports.
Input: CSV with at least two columns for impressions and engagements.
Output: avg, median, top post engagement rate, and post count.

Usage:
  python engagement-tracker.py twitter_export.csv impressions engagements
"""
import csv
import statistics
import sys


def engagement_summary(csv_path: str, impressions_col: str, engagements_col: str) -> dict:
    rates = []
    with open(csv_path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            imp = int(row.get(impressions_col, 0) or 0)
            eng = int(row.get(engagements_col, 0) or 0)
            if imp > 0:
                rates.append(eng / imp * 100)
    if not rates:
        return {"error": "No rows with non-zero impressions found"}
    return {
        "avg_engagement_rate": round(statistics.mean(rates), 2),
        "median_engagement_rate": round(statistics.median(rates), 2),
        "top_post_rate": round(max(rates), 2),
        "posts_analyzed": len(rates),
    }


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python engagement-tracker.py <csv_path> <impressions_col> <engagements_col>")
        sys.exit(1)
    result = engagement_summary(sys.argv[1], sys.argv[2], sys.argv[3])
    for k, v in result.items():
        print(f"{k}: {v}")
