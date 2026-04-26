"""
Parse a Shield analytics CSV export to find top N posts by engagement rate.

Input:  CSV file exported from shieldapp.ai
Output: List of top posts with engagement rate, impressions, and truncated text

Usage:
    python top-posts-analyzer.py shield_export.csv
    python top-posts-analyzer.py shield_export.csv --top 10
"""

import csv
import sys
from argparse import ArgumentParser


def top_posts(csv_path: str, n: int = 5) -> list[dict]:
    """Return top N posts sorted by engagement rate descending."""
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            impressions = int(row.get("impressions", 0) or 0)
            engagements = int(row.get("engagements", 0) or 0)
            if impressions > 0:
                row["eng_rate"] = engagements / impressions
                rows.append(row)
    rows.sort(key=lambda r: r["eng_rate"], reverse=True)
    return rows[:n]


def main():
    parser = ArgumentParser(description="Find top LinkedIn posts by engagement rate")
    parser.add_argument("csv_path", help="Path to Shield analytics CSV export")
    parser.add_argument("--top", type=int, default=5, help="Number of posts to show")
    args = parser.parse_args()

    posts = top_posts(args.csv_path, args.top)
    if not posts:
        print("No posts found with impressions > 0")
        sys.exit(1)

    for i, post in enumerate(posts, 1):
        text = post.get("text", "")[:100].replace("\n", " ")
        print(f"{i}. {post['eng_rate']:.1%} eng | {post.get('impressions', 0)} impr | {text}...")


if __name__ == "__main__":
    main()
