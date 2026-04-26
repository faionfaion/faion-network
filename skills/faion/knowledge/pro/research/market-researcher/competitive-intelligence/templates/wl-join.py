#!/usr/bin/env python3
"""
wl_join.py — join win/loss + pricing + positioning event streams into competitive-analysis.md

Input files (NDJSON, one JSON object per line):
  wl_events.ndjson      — {closed_at, outcome, competitor_won, primary_reason, confidence, segment}
  pricing_events.ndjson — {competitor, effective_annual_cost_delta_usd, change_type, confidence}
  positioning_events.ndjson — {competitor, claimed_category, jtbd_extracted}

Output: .aidocs/product_docs/competitive-analysis.md
Filters: confidence < 3 rows are dropped; n < 5 per competitor is dropped (anecdote, not data)
"""
import json
import pathlib
import collections
import datetime

WL = [json.loads(line) for line in open("wl_events.ndjson")]
PRICE = [json.loads(line) for line in open("pricing_events.ndjson")]
POS = [json.loads(line) for line in open("positioning_events.ndjson")]

# Win-rate per competitor, last 90 days
cutoff = (datetime.datetime.utcnow() - datetime.timedelta(days=90)).isoformat()
recent = [d for d in WL if d.get("closed_at", "") >= cutoff]
by_comp: dict[str, dict] = collections.defaultdict(
    lambda: {"won": 0, "lost": 0, "no_decision": 0, "reasons": []}
)

for d in recent:
    if d.get("confidence", 0) < 3:
        continue  # drop low-confidence rows
    comp = d.get("competitor_won") or "no-competitor"
    outcome = d.get("outcome", "")
    if outcome == "won":
        by_comp[comp]["won"] += 1
    elif outcome == "lost":
        by_comp[comp]["lost"] += 1
        by_comp[comp]["reasons"].append(d.get("primary_reason", "other"))
    elif outcome == "no_decision":
        by_comp[comp]["no_decision"] += 1  # tracked separately, not in win-rate denominator

rows = []
for comp, s in by_comp.items():
    n_competitive = s["won"] + s["lost"]  # exclude no_decision from win-rate denominator
    if n_competitive < 5:
        continue  # n<5 is anecdote, not data
    win_rate = s["won"] / n_competitive
    top_reason = collections.Counter(s["reasons"]).most_common(1)
    price_delta = next(
        (p.get("effective_annual_cost_delta_usd") for p in PRICE if p.get("competitor") == comp and p.get("confidence", 0) >= 3),
        None,
    )
    position = next(
        (p.get("claimed_category") for p in POS if p.get("competitor") == comp),
        "?",
    )
    rows.append((comp, n_competitive, win_rate, top_reason[0][0] if top_reason else "?", price_delta, position, s["no_decision"]))

# Sort worst win-rate first (highest competitive threat)
rows.sort(key=lambda r: r[2])

out = pathlib.Path(".aidocs/product_docs/competitive-analysis.md")
out.parent.mkdir(parents=True, exist_ok=True)
today = datetime.date.today().isoformat()
with out.open("w") as f:
    f.write(f"# Competitive Analysis ({today})\n\n")
    f.write("_Win-rate excludes no_decision outcomes. Rows with n<5 or confidence<3 omitted._\n\n")
    f.write("| Competitor | n | Win-rate | Top loss reason | Price delta (USD/yr) | Position | No-decision |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    for comp, n, wr, r, pd, pos, nd in rows:
        f.write(f"| {comp} | {n} | {wr:.0%} | {r} | {pd or '?'} | {pos} | {nd} |\n")

print(f"wrote {out} — {len(rows)} competitors, 90-day window ending {today}")
