#!/usr/bin/env python3
"""comms_audit.py — list stakeholders due an update this week.

Reads comms/plan.yaml; prints overdue communications and exits non-zero if any found.
Wire into a weekly cron or GitHub Action; failures open a PM task.

plan.yaml structure:
  communications:
    - stakeholder: "Sponsor"
      frequency: weekly   # daily|weekly|biweekly|monthly|quarterly
      last_sent: "2026-04-19"
      channel: email
      owner: PM
"""
from __future__ import annotations
import datetime as dt
import pathlib
import sys
import yaml

CADENCE_DAYS: dict[str, int] = {
    "daily": 1,
    "weekly": 7,
    "biweekly": 14,
    "monthly": 30,
    "quarterly": 90,
}


def main(plan_path: str = "comms/plan.yaml") -> int:
    path = pathlib.Path(plan_path)
    if not path.exists():
        print(f"ERROR: {plan_path} not found", file=sys.stderr)
        return 1
    plan = yaml.safe_load(path.read_text())
    today = dt.date.today()
    overdue: list[str] = []
    for entry in plan.get("communications", []):
        last = entry.get("last_sent")
        stakeholder = entry.get("stakeholder", "unknown")
        frequency = entry.get("frequency", "weekly")
        if last is None:
            overdue.append(f"{stakeholder} ({frequency}): never sent")
            continue
        last_date = dt.date.fromisoformat(str(last))
        gap = (today - last_date).days
        max_gap = CADENCE_DAYS.get(frequency, 7)
        if gap > max_gap:
            overdue.append(
                f"{stakeholder} ({frequency}): {gap}d since {last_date}"
                f" — owner: {entry.get('owner', 'unset')}"
            )
    if overdue:
        print("OVERDUE COMMUNICATIONS:")
        for line in overdue:
            print(f"  {line}")
        return 1
    print("All communications current.")
    return 0


if __name__ == "__main__":
    plan = sys.argv[1] if len(sys.argv) > 1 else "comms/plan.yaml"
    sys.exit(main(plan))
