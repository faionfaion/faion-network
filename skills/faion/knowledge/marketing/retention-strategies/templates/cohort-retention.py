"""
cohort_retention.py — D-N retention by signup week.

Input:  events DataFrame with columns: user_id (str), timestamp (datetime), event (str)
Output: DataFrame with columns: cohort (str), size (int), D1, D7, D14, D30 (float ratios)

Usage:
    import pandas as pd
    df = pd.read_csv("events.csv", parse_dates=["timestamp"])
    result = cohort_retention(df, action_event="active")
    print(result.to_markdown())
"""
import pandas as pd


def cohort_retention(
    events: pd.DataFrame,
    action_event: str = "active",
    windows: tuple[int, ...] = (1, 7, 14, 30),
) -> pd.DataFrame:
    """Return D-N retention ratios by signup week cohort."""
    df = events.copy()
    df["signup_week"] = (
        df.groupby("user_id")["timestamp"].transform("min").dt.to_period("W")
    )
    df["days_since_signup"] = (
        df["timestamp"] - df.groupby("user_id")["timestamp"].transform("min")
    ).dt.days

    out = []
    active = df[df["event"] == action_event]
    for cohort_week, group in active.groupby("signup_week"):
        size = group["user_id"].nunique()
        row: dict = {"cohort": str(cohort_week), "size": size}
        for n in windows:
            retained = group[group["days_since_signup"] <= n]["user_id"].nunique()
            row[f"D{n}"] = round(retained / size, 3) if size else 0.0
        out.append(row)
    return pd.DataFrame(out)
