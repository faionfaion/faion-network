#!/usr/bin/env python3
"""risk-audit.py — flag stale, high-priority, and no-owner risks in a CSV register.

Usage: python risk-audit.py risks.csv
CSV must have columns: id, score, last_update (ISO date), status, owner.
Exit 0 = all clear, exit 1 = issues found.
"""
import csv
import datetime
import sys

today = datetime.date.today()
found = False

with open(sys.argv[1]) as f:
    for r in csv.DictReader(f):
        score = int(r.get("score") or 0)
        upd = r.get("last_update", "")
        try:
            d = datetime.date.fromisoformat(upd)
        except (ValueError, AttributeError):
            d = today
        stale_days = (today - d).days
        flags = []
        if score >= 15:
            flags.append("HIGH_PRIORITY")
        if stale_days > 14 and r.get("status", "").lower() == "open":
            flags.append(f"STALE_{stale_days}d")
        if not r.get("owner", "").strip():
            flags.append("NO_OWNER")
        if flags:
            print(f"{r['id']}\t{','.join(flags)}")
            found = True

sys.exit(1 if found else 0)
