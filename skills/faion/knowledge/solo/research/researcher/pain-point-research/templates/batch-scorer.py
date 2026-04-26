#!/usr/bin/env python3
"""
Pain point batch scorer.
Input (stdin): JSON list of pain points with fields:
  quote, url, source, category, freq (1-5), sev (1-5), reach (1-5), spend (1-5), alt (1-5)
Output (stdout): CSV with id, category, quote (truncated), url, score sorted descending.
Usage: cat pain_points.json | python3 batch-scorer.py > pain_points.csv
"""
import json
import csv
import sys

WEIGHTS = {"freq": 0.30, "sev": 0.25, "reach": 0.20, "spend": 0.15, "alt": 0.10}

items = json.load(sys.stdin)

writer = csv.writer(sys.stdout)
writer.writerow(["id", "category", "quote", "url", "score"])

scored = []
for i, item in enumerate(items, 1):
    score = sum(WEIGHTS[k] * float(item.get(k, 0)) for k in WEIGHTS)
    scored.append((i, item, round(score, 2)))

scored.sort(key=lambda x: x[2], reverse=True)

for i, item, score in scored:
    writer.writerow([
        f"PP-{i:03}",
        item.get("category", ""),
        item.get("quote", "")[:200],
        item.get("url", ""),
        score,
    ])
