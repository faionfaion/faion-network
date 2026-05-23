# purpose: Reminder cadence scheduler
# consumes: participants list with timezones
# produces: scheduled push + SMS jobs
# depends-on: stdlib + provider SDK
# token-budget-impact: ~250
"""diary-reminders.py — schedule push + SMS reminders per participant timezone."""
from __future__ import annotations
import datetime
import json
from pathlib import Path

def schedule(participants_path: str) -> None:
    participants = json.loads(Path(participants_path).read_text())
    for p in participants:
        # 22:00 local push + 23:30 SMS fallback if no entry by then
        print(f"schedule push {p['id']} @22:00 {p['tz']}")
        print(f"schedule sms-fallback {p['id']} @23:30 {p['tz']}")

if __name__ == "__main__":
    import sys
    schedule(sys.argv[1])
