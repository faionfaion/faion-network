"""engagement_due.py — list stakeholders past their engagement cadence.

Usage:
  python engagement_due.py stakeholders/register.yaml
  python engagement_due.py  # defaults to stakeholders/register.yaml

register.yaml shape:
  stakeholders:
    - id: S-01
      name: Alice Chen
      cadence: weekly
      last_engaged: "2026-04-10"
    - id: S-02
      name: Bob Kowalski
      cadence: monthly
      last_engaged: null
"""

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
            due.append(f"{s['id']}  {s['name']:<30}  never engaged ({cadence})")
            continue

        gap = (today - dt.date.fromisoformat(str(last))).days
        if gap > max_gap:
            due.append(
                f"{s['id']}  {s['name']:<30}  {gap}d > {max_gap}d ({cadence})"
            )

    sys.stdout.write("\n".join(due) + "\n" if due else "All stakeholders current.\n")
    return 1 if due else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
