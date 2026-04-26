#!/usr/bin/env python3
"""flow_metrics.py — Lead Time, Cycle Time, and Throughput from transitions CSV.

Input CSV columns required: issue_id, status, ts (ISO 8601 timestamp)
Statuses required: "To Do", "In Progress", "Done"

Usage:
    python3 flow_metrics.py transitions.csv
"""
from __future__ import annotations

import sys
import pandas as pd


def main(path: str) -> int:
    df = pd.read_csv(path, parse_dates=["ts"])

    # Pivot to get first timestamp each issue entered each status
    pivot = df.pivot_table(
        index="issue_id", columns="status", values="ts", aggfunc="min"
    )

    required = {"To Do", "In Progress", "Done"}
    if not required.issubset(pivot.columns):
        missing = required - set(pivot.columns)
        print(f"Missing required statuses: {missing}", file=sys.stderr)
        return 2

    pivot["lead_time_days"] = (
        pivot["Done"] - pivot["To Do"]
    ).dt.total_seconds() / 86400

    pivot["cycle_time_days"] = (
        pivot["Done"] - pivot["In Progress"]
    ).dt.total_seconds() / 86400

    summary = (
        pivot[["lead_time_days", "cycle_time_days"]]
        .dropna()
        .describe(percentiles=[0.5, 0.85, 0.95])
    )
    print("=== Lead Time and Cycle Time ===")
    print(summary.to_string())

    # Throughput per ISO week
    weekly = (
        df[df["status"] == "Done"]
        .set_index("ts")
        .resample("W")["issue_id"]
        .nunique()
    )
    print("\n=== Weekly Throughput (items/week) ===")
    print(weekly.to_string())
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <transitions.csv>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
