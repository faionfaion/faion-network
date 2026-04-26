"""
TikTok Analytics CSV Processor
Input: TikTok Analytics export CSV (download from TikTok Studio > Analytics > Video)
Output: Top 5 videos by views with avg watch percentage and share count

Usage: python analytics-processor.py <path-to-analytics.csv>
"""

import csv
import json
import sys


def analyze_analytics(filepath: str) -> dict:
    videos = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                views = int(row.get("Video Views", 0) or 0)
                watch_pct_raw = row.get("Average Watch Time", "0") or "0"
                watch_pct = float(watch_pct_raw.replace("%", "").strip() or 0)
                shares = int(row.get("Shares", 0) or 0)
            except (ValueError, AttributeError):
                continue
            videos.append({
                "title": row.get("Video Title", "")[:60],
                "views": views,
                "avg_watch_pct": watch_pct,
                "shares": shares,
            })

    videos.sort(key=lambda x: x["views"], reverse=True)
    top5 = videos[:5]
    avg_completion = (
        sum(v["avg_watch_pct"] for v in top5) / len(top5) if top5 else 0
    )

    return {
        "top5": top5,
        "avg_completion_top5": round(avg_completion, 1),
        "total_videos_analyzed": len(videos),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analytics-processor.py <path-to-csv>")
        sys.exit(1)
    result = analyze_analytics(sys.argv[1])
    print(json.dumps(result, indent=2))
