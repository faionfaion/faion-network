#!/usr/bin/env python3
"""Detect stalled stakeholders by comparing last-touch date against
cadence thresholds per power/interest quadrant.

Usage: engagement-drift.py <register.yaml> <comms-log.yaml>

register.yaml items: [{id, name, quadrant: manage-closely|keep-satisfied|keep-informed|monitor}]
comms-log.yaml items: [{stakeholder_id, date: YYYY-MM-DD}]
"""
import sys
import yaml
from datetime import date, timedelta

CADENCE_DAYS = {
    "manage-closely": 7,
    "keep-satisfied": 14,
    "keep-informed": 7,
    "monitor": 30,
}


def main(reg_path, log_path):
    register = yaml.safe_load(open(reg_path))
    touches = yaml.safe_load(open(log_path)) or []

    last_touch: dict[str, date] = {}
    for t in touches:
        d = date.fromisoformat(str(t["date"]))
        sid = t["stakeholder_id"]
        last_touch[sid] = max(last_touch.get(sid, d), d)

    today = date.today()
    drifted = []
    for s in register:
        sid = s["id"]
        quadrant = s.get("quadrant", "monitor")
        max_gap = CADENCE_DAYS.get(quadrant, 30)
        last = last_touch.get(sid, today - timedelta(days=999))
        gap = (today - last).days
        if gap > max_gap:
            drifted.append(
                f"[DRIFT] {sid} '{s['name']}' quadrant={quadrant} "
                f"gap={gap}d (threshold={max_gap}d)"
            )

    if drifted:
        for line in drifted:
            print(line)
        sys.exit(1)
    print("No drift detected")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: engagement-drift.py <register.yaml> <comms-log.yaml>")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
