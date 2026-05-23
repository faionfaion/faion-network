#!/usr/bin/env python3
"""engagement_due.py — flag stakeholders past their engagement cadence.

Usage:  python engagement_due.py [path/to/register.yaml]
Exit:   1 if any stakeholder is overdue (wire to CI for weekly check).
"""
from __future__ import annotations
import datetime as dt
import pathlib
import sys
import yaml

CADENCE_DAYS = {
    "daily": 1,
    "weekly": 7,
    "biweekly": 14,
    "monthly": 30,
    "quarterly": 90,
    "release": 60,
}


def main(path: str = "stakeholders/register.yaml") -> int:
    data = yaml.safe_load(pathlib.Path(path).read_text())
    today = dt.date.today()
    due: list[str] = []
    for s in data.get("stakeholders", []):
        cadence = s.get("cadence", "monthly")
        last = s.get("last_engaged")
        max_gap = CADENCE_DAYS.get(cadence, 30)
        if last is None:
            due.append(f"{s['id']} {s['name']:<25} never engaged ({cadence})")
            continue
        gap = (today - dt.date.fromisoformat(str(last))).days
        if gap > max_gap:
            due.append(f"{s['id']} {s['name']:<25} {gap}d > {max_gap}d ({cadence})")
    if due:
        sys.stdout.write("\n".join(due) + "\n")
        return 1
    sys.stdout.write("All engagements current.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
