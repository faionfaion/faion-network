"""
Validate a proposed Product Hunt launch datetime.
Requirements: 12:01 AM Pacific Time, Tuesday-Thursday.
Warns on weekends, Mondays, and Fridays.

Usage:
  python check-launch-timing.py "2026-06-03T00:01:00-07:00"
"""
import sys
from datetime import datetime

try:
    import pytz
    HAS_PYTZ = True
except ImportError:
    HAS_PYTZ = False


def check_launch_timing(iso_datetime_str: str) -> dict:
    """Evaluate a proposed PH launch time."""
    if HAS_PYTZ:
        pt = pytz.timezone("America/Los_Angeles")
        dt = datetime.fromisoformat(iso_datetime_str).astimezone(pt)
    else:
        # Fallback: assume input is already in PT offset
        dt = datetime.fromisoformat(iso_datetime_str)

    issues = []
    if dt.hour != 0 or dt.minute != 1:
        issues.append(
            f"Not 12:01 AM PT — launches lose ranking hours (got {dt.strftime('%H:%M')} PT)"
        )
    if dt.weekday() not in (1, 2, 3):  # Tue=1, Wed=2, Thu=3
        day_name = dt.strftime("%A")
        issues.append(
            f"Not Tue-Thu — {day_name}s have lower active user counts on PH"
        )

    return {
        "ok": len(issues) == 0,
        "issues": issues,
        "local_time_pt": dt.isoformat(),
        "day_of_week": dt.strftime("%A"),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check-launch-timing.py <iso_datetime>")
        print("Example: python check-launch-timing.py 2026-06-03T00:01:00-07:00")
        sys.exit(1)
    result = check_launch_timing(sys.argv[1])
    print(f"Launch time (PT): {result['local_time_pt']}")
    print(f"Day of week: {result['day_of_week']}")
    if result["ok"]:
        print("Timing OK — 12:01 AM PT on a weekday")
    else:
        print("Timing issues:")
        for issue in result["issues"]:
            print(f"  - {issue}")
