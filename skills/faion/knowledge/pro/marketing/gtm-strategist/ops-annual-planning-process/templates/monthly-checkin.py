"""
Monthly planning check-in: actual vs expected KR progress.

Inputs:
  quarter_targets -- dict of {kr_name: numeric_target}
  actuals         -- dict of {kr_name: current_actual}
  today           -- date object for this check-in

Output:
  dict with as_of, quarter_progress_pct, items (list of kr status), off_track list
"""

from datetime import date


def monthly_checkin(
    quarter_targets: dict, actuals: dict, today: date
) -> dict:
    items = []
    # Progress through the current quarter (0.0 to 1.0)
    month_in_quarter = (today.month - 1) % 3  # 0, 1, or 2
    day_fraction = today.day / 30.0
    quarter_progress = (month_in_quarter + day_fraction) / 3.0

    for kr, target in quarter_targets.items():
        actual = actuals.get(kr, 0)
        expected = target * quarter_progress
        delta = actual - expected
        if delta >= -0.05 * target:
            status = "on_track"
        elif delta >= -0.15 * target:
            status = "at_risk"
        else:
            status = "off_track"
        items.append({
            "kr": kr,
            "actual": actual,
            "expected": round(expected, 2),
            "target": target,
            "status": status,
        })

    return {
        "as_of": today.isoformat(),
        "quarter_progress_pct": round(quarter_progress * 100, 1),
        "items": items,
        "off_track": [i["kr"] for i in items if i["status"] == "off_track"],
    }


# Example usage:
# monthly_checkin(
#     quarter_targets={"arr_usd": 100000, "customers": 200},
#     actuals={"arr_usd": 62000, "customers": 130},
#     today=date(2025, 2, 15),
# )
