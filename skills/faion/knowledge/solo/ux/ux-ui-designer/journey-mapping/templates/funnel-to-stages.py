"""
Convert funnel analytics CSV to stage summaries for agent journey map ingestion.

Input CSV columns: stage, sessions, drop_off_pct, avg_time_sec
Output: JSON list of stage summary dicts for use as agent context.

Usage:
    python funnel-to-stages.py funnel.csv

Example CSV:
    stage,sessions,drop_off_pct,avg_time_sec
    Home,10000,15,45
    Product Page,8500,22,120
    Cart,6630,45,60
    Checkout,3647,38,180
    Confirmation,2261,0,30
"""

import csv
import json
import sys


def summarize(path: str) -> list:
    stages = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            drop_pct = float(row["drop_off_pct"])
            stages.append({
                "stage": row["stage"],
                "sessions": int(row["sessions"]),
                "drop_off_pct": drop_pct,
                "avg_time_sec": int(row["avg_time_sec"]),
                "risk": "high" if drop_pct > 30 else "normal",
                "note": (
                    f"High drop-off ({drop_pct:.0f}%) — likely pain point. Investigate."
                    if drop_pct > 30
                    else f"Normal drop-off ({drop_pct:.0f}%)."
                ),
            })
    return stages


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python funnel-to-stages.py <funnel.csv>")
        sys.exit(1)
    result = summarize(sys.argv[1])
    print(json.dumps(result, indent=2))

    high_risk = [s for s in result if s["risk"] == "high"]
    if high_risk:
        print(f"\nHigh-risk stages for journey map priority: {[s['stage'] for s in high_risk]}")


if __name__ == "__main__":
    main()
