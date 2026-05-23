#!/usr/bin/env python3
"""capacity.py — compute effective hours per person per week.

Inputs (YAML files):
  roster.yaml   — {name: {hours_week: 40, role: "be"}}
  pto.yaml      — {name: ["YYYY-MM-DD", ...]}  (ISO dates of full PTO days)
  meetings.yaml — {name: <weekly_meeting_hours>}

Output: JSON {person: effective_hours} for the target week.
Usage:  python capacity.py [YYYY-MM-DD]  (Monday of target week; defaults to next Monday)
"""
from __future__ import annotations
import json
import sys
from datetime import date, timedelta
import yaml

EFFECTIVE_RATE = 0.80   # 80% of nominal = standard knowledge-work cap
BUFFER_HOURS = 4        # weekly interruption buffer


def next_monday(from_date: date = date.today()) -> date:
    days_ahead = 7 - from_date.weekday() if from_date.weekday() != 0 else 0
    return from_date + timedelta(days=days_ahead or 7)


def week_days(monday: date) -> list[date]:
    return [monday + timedelta(i) for i in range(5)]


def effective_hours(
    person: str,
    monday: date,
    roster: dict,
    pto: dict,
    meetings: dict,
) -> float:
    nominal = roster[person]["hours_week"]
    pto_days = sum(1 for d in week_days(monday) if d.isoformat() in pto.get(person, []))
    base = nominal * (5 - pto_days) / 5
    result = max(0.0, base * EFFECTIVE_RATE - meetings.get(person, 0) - BUFFER_HOURS)
    return round(result, 1)


def main(target_week: str | None = None) -> int:
    monday = date.fromisoformat(target_week) if target_week else next_monday()
    roster = yaml.safe_load(open("roster.yaml"))
    pto = yaml.safe_load(open("pto.yaml"))
    meetings = yaml.safe_load(open("meetings.yaml"))
    out = {p: effective_hours(p, monday, roster, pto, meetings) for p in roster}
    print(json.dumps({"week": monday.isoformat(), "capacity_h": out}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
