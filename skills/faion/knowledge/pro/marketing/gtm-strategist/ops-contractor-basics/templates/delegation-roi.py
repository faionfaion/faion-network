"""
Delegation ROI calculator.

Inputs:
  my_rate              -- founder's effective hourly rate ($)
  task_hours_per_week  -- hours founder currently spends on this task per week
  contractor_rate      -- contractor's hourly rate ($)
  contractor_hours     -- hours contractor takes to do the same task per week
  onboarding_hours     -- estimated hours to onboard the contractor (default 8)

Output:
  dict with weekly_save, annual_save, payback_weeks, delegate recommendation
"""


def delegation_roi(
    my_rate: float,
    task_hours_per_week: float,
    contractor_rate: float,
    contractor_hours: float,
    onboarding_hours: float = 8.0,
) -> dict:
    my_cost_weekly = my_rate * task_hours_per_week
    contractor_cost_weekly = contractor_rate * contractor_hours
    weekly_save = my_cost_weekly - contractor_cost_weekly

    if weekly_save <= 0:
        return {
            "weekly_save": round(weekly_save, 2),
            "annual_save": round(weekly_save * 50, 2),
            "payback_weeks": None,
            "delegate": False,
            "note": "No financial ROI at these rates. Delegation may still be worth it for time freedom.",
        }

    onboarding_cost = my_rate * onboarding_hours
    payback_weeks = round(onboarding_cost / weekly_save, 1)

    return {
        "weekly_save": round(weekly_save, 2),
        "annual_save": round(weekly_save * 50, 2),
        "payback_weeks": payback_weeks,
        "delegate": contractor_rate < my_rate * 0.6,
        "note": (
            "Recommended if contractor rate < 60% of your rate. "
            "Always run a paid test task before committing."
        ),
    }


# Example:
# delegation_roi(my_rate=100, task_hours_per_week=5,
#                contractor_rate=30, contractor_hours=4)
# {'weekly_save': 380, 'annual_save': 19000, 'payback_weeks': 2.1, 'delegate': True}
