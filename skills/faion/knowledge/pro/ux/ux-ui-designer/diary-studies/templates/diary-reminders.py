"""
diary-reminders.py — emit per-participant reminder schedule with early-study weighting.

Usage: python diary-reminders.py <study_start_date> <study_days> <participants.json>
  study_start_date: ISO8601 date string (e.g. 2026-05-01)
  study_days: integer
  participants.json: [{"id": "p01", "channel": "sms|email|push", "tz": "Europe/Lisbon"}]

Output: JSON array of reminder events to stdout.
"""
import json
import sys
import datetime as dt


def build_schedule(study_start: dt.date, days: int, participants: list) -> list:
    schedule = []
    for p in participants:
        for d in range(days):
            date = study_start + dt.timedelta(days=d)
            # Heavy reminders days 0-2 (habit-building), every 3rd day mid-study,
            # always on last day. Vary prompt index to avoid repetition.
            should_send = d < 3 or d % 3 == 0 or d == days - 1
            if should_send:
                schedule.append({
                    "pid": p["id"],
                    "channel": p["channel"],
                    "tz": p["tz"],
                    "date": date.isoformat(),
                    "prompt_index": d % 5,  # rotate across 5 prompt variants
                    "type": "prompt" if d < days - 1 else "exit-reminder",
                })
    return schedule


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)

    start = dt.date.fromisoformat(sys.argv[1])
    days = int(sys.argv[2])
    participants = json.load(open(sys.argv[3]))

    result = build_schedule(start, days, participants)
    print(json.dumps(result, indent=2))
