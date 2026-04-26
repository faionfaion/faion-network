# basic_cohort.py — quick acquisition cohort table from CSV exports
# Input: users.csv (user_id, signup_date), events.csv (user_id, event_type, event_date)
# Output: pivot table: cohort_week x [D1, D7, D30, D60, D90] retention percentages

import pandas as pd

users = pd.read_csv("users.csv", parse_dates=["signup_date"])
events = pd.read_csv("events.csv", parse_dates=["event_date"])
events = events[events.event_type == "login"]  # change to your retention-defining event

# Weekly cohorts
users["cohort"] = users.signup_date.dt.to_period("W")
df = events.merge(users, on="user_id")
df["d"] = (df.event_date - df.signup_date).dt.days

# Filter to measurement days; add/remove as needed
measurement_days = [1, 7, 30, 60, 90]
df = df[df.d.isin(measurement_days)]

active = df.groupby(["cohort", "d"]).user_id.nunique().reset_index(name="active")
size = users.groupby("cohort").user_id.nunique().reset_index(name="size")
ret = active.merge(size, on="cohort")
ret["pct"] = (ret.active / ret["size"] * 100).round(1)

table = ret.pivot(index="cohort", columns="d", values="pct")
# Add cohort size column
table.insert(0, "size", size.set_index("cohort")["size"])
print(table.to_string())
