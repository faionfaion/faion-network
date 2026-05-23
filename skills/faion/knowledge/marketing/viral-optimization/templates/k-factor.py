# k_factor.py — compute K-factor and cycle time from event stream CSV
# Input: events.csv with columns: ts (datetime), type, inviter_id, ref_token
# Output: i, c, K, cycle_time median printed to stdout

import pandas as pd

ev = pd.read_csv("events.csv", parse_dates=["ts"])
inv = ev[ev.type == "invite_sent"]
sig = ev[ev.type == "invitee_signup"]

# Average invites per inviter
i = inv.groupby("inviter_id").size().mean()

# Conversion: signups matched to invite tokens
matched = sig.merge(inv, on="ref_token", suffixes=("_s", "_i"))
c = len(matched) / max(len(inv), 1)

# Cycle time: days from invite_sent to invitee_signup
cycle = (matched.ts_s - matched.ts_i).dt.days
K = i * c

print(f"i={i:.2f}  c={c:.2%}  K={K:.3f}  cycle_p50={cycle.median():.1f}d")

# Decay check: K by inviter cohort week
inv = inv.copy()
inv["cohort"] = inv.ts.dt.to_period("W")
print("\nInvite volume by cohort:")
print(inv.groupby("cohort").size().tail(8).to_string())
