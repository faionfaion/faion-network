# cohort_matrix.py — compute acquisition cohort retention matrix from event DataFrame
# Input: events DataFrame with columns: user_id, event_date, signup_date
# Output: retention matrix as DataFrame (cohort x day_n, values = retention rate 0..1)

import pandas as pd


def cohort_matrix(
    events: pd.DataFrame,
    user_col: str = "user_id",
    date_col: str = "event_date",
    signup_col: str = "signup_date",
    max_day: int = 30,
    min_cohort_size: int = 50,
) -> pd.DataFrame:
    """
    Returns a cohort x day_n retention matrix.
    Suppresses cohorts with fewer than min_cohort_size users.
    """
    events = events.copy()
    events["day_n"] = (events[date_col] - events[signup_col]).dt.days
    events = events[(events["day_n"] >= 0) & (events["day_n"] <= max_day)]

    cohort_size = (
        events.groupby(signup_col)[user_col].nunique().rename("cohort_size")
    )
    retained = (
        events.groupby([signup_col, "day_n"])[user_col]
        .nunique()
        .unstack(fill_value=0)
    )
    matrix = retained.div(cohort_size, axis=0).round(3)

    # Suppress small cohorts
    mask = cohort_size >= min_cohort_size
    return matrix.loc[mask]
