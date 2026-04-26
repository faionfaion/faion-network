#!/usr/bin/env python3
"""
pm-attention-diff.py — flag mismatch between PM time and stakeholder weight.
Inputs:
  register.md  — PM stakeholder register (table format with Power/Interest columns)
  calendar.csv — rows: stakeholder_name, minutes_spent_last_30d
Usage: python pm-attention-diff.py register.md calendar.csv
A UNDER on a high-power Resistor is the bug to fix this week.
"""
import sys, csv, pathlib

reg = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
rows = [r for r in reg.splitlines() if r.startswith("|") and "---" not in r]
hdr = [c.strip().lower() for c in rows[0].strip("|").split("|")]
score = {"high": 3, "medium": 2, "low": 1, "h": 3, "m": 2, "l": 1}
weight = {}
for r in rows[1:]:
    cells = [c.strip() for c in r.strip("|").split("|")]
    if len(cells) < len(hdr):
        continue
    name = cells[hdr.index("name")].strip()
    p = score.get(cells[hdr.index("power")].lower(), 0)
    i = score.get(cells[hdr.index("interest")].lower(), 0)
    if name and p and i:
        weight[name] = p * i

mins = {}
with open(sys.argv[2]) as fh:
    for row in csv.DictReader(fh):
        mins[row["stakeholder_name"]] = (
            mins.get(row["stakeholder_name"], 0) + int(row["minutes_spent_last_30d"])
        )

total_w = sum(weight.values()) or 1
total_m = sum(mins.values()) or 1
print(f"{'Stakeholder':<28} {'Weight%':>8} {'Time%':>8} {'Delta':>8}")
for name, w in sorted(weight.items(), key=lambda x: -x[1]):
    wp = 100 * w / total_w
    tp = 100 * mins.get(name, 0) / total_m
    delta = tp - wp
    flag = "  OVER" if delta > 15 else "  UNDER" if delta < -15 else ""
    print(f"{name:<28} {wp:>7.1f}% {tp:>7.1f}% {delta:>+7.1f}%{flag}")
