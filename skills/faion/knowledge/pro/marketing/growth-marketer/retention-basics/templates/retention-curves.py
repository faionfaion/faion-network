# retention_curves.py — DAU/MAU ratio + 8-week cohort retention curve
# Input: events.csv with columns: user_id, event_date, event_type
# Output: DAU/MAU ratio for last 7 days + weekly retention curve (W0..W7)

import pandas as pd

ev = pd.read_csv("events.csv", parse_dates=["event_date"])
ev = ev[ev.event_type == "core_action"]  # replace with your retention metric

# DAU/MAU rolling ratio
dau = ev.groupby(ev.event_date.dt.date).user_id.nunique()
mau = ev.set_index("event_date").user_id.resample("D").apply(
    lambda s: ev[
        (ev.event_date >= s.name - pd.Timedelta("30D"))
        & (ev.event_date <= s.name)
    ].user_id.nunique()
)
print("DAU/MAU last 7d:", (dau / mau).tail(7).round(2).to_dict())

# Weekly retention curve (W0..W7)
ev["week"] = ev.event_date.dt.to_period("W")
first = ev.groupby("user_id").event_date.min().dt.to_period("W").rename("cohort")
df = ev.merge(first, on="user_id")
df["week_offset"] = (df.week - df.cohort).apply(lambda x: x.n)
curve = (
    df[df.week_offset.between(0, 7)]
    .groupby(["cohort", "week_offset"])
    .user_id.nunique()
    .unstack()
)
print(curve.div(curve[0], axis=0).round(2).tail(8))
