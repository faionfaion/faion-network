#!/usr/bin/env python3
"""cycle-stats.py — compute throughput and cycle-time stats from JSONL of issues.

Input JSONL: one JSON object per line with fields:
    state: str          — "Done", "In Progress", etc.
    resolved_at: str    — ISO 8601 timestamp when state became "Done"
    started_at: str     — ISO 8601 timestamp when state became "In Progress" (optional)

Computes throughput over the last 28 days and cycle-time percentiles.

Usage:
    cat issues.jsonl | python3 cycle-stats.py
    python3 cycle-stats.py < issues.jsonl
"""
from __future__ import annotations

import json
import statistics
import sys
from datetime import datetime, timedelta, timezone


def main() -> int:
    issues = [json.loads(line) for line in sys.stdin if line.strip()]
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=28)

    done = [
        i for i in issues
        if i.get("state") == "Done"
        and datetime.fromisoformat(i["resolved_at"]).replace(tzinfo=timezone.utc) > cutoff
    ]

    cycle_days = [
        (
            datetime.fromisoformat(i["resolved_at"]).replace(tzinfo=timezone.utc)
            - datetime.fromisoformat(i["started_at"]).replace(tzinfo=timezone.utc)
        ).total_seconds() / 86400
        for i in done
        if i.get("started_at")
    ]

    weekly = len(done) / 4
    print(f"throughput_28d={len(done)}  weekly_avg={weekly:.1f}")

    if cycle_days:
        p50 = statistics.median(cycle_days)
        sorted_days = sorted(cycle_days)
        p85_idx = int(len(sorted_days) * 0.85)
        p85 = sorted_days[min(p85_idx, len(sorted_days) - 1)]
        print(
            f"cycle_p50={p50:.1f}d  "
            f"cycle_p85={p85:.1f}d  "
            f"cycle_max={max(cycle_days):.1f}d  "
            f"n={len(cycle_days)}"
        )
    else:
        print("No cycle-time data (missing started_at fields).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
