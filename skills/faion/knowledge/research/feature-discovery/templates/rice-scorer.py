#!/usr/bin/env python3
"""
RICE feature scorer.
Input: CSV file path as first argument.
  Required columns: feature, reach, impact, confidence, effort
  - reach: integer (users per quarter from telemetry — not estimates)
  - impact: float (0.25, 0.5, 1, 2, or 3)
  - confidence: integer (50, 80, or 100 — must have evidence citation)
  - effort: float (person-weeks; minimum 0.1 to avoid division by zero)
Output (stdout): sorted RICE scores, highest first.
Usage: python3 rice-scorer.py features.csv
"""
import csv
import sys

if len(sys.argv) < 2:
    print("Usage: python3 rice-scorer.py features.csv", file=sys.stderr)
    sys.exit(1)

with open(sys.argv[1]) as f:
    rows = list(csv.DictReader(f))

scored = []
for row in rows:
    try:
        reach = float(row["reach"])
        impact = float(row["impact"])
        confidence = float(row["confidence"]) / 100
        effort = max(float(row["effort"]), 0.1)
        rice = (reach * impact * confidence) / effort
        scored.append((row["feature"], round(rice, 1), reach, impact, confidence * 100, effort))
    except (KeyError, ValueError) as e:
        print(f"Skipping row {row.get('feature', '?')}: {e}", file=sys.stderr)

scored.sort(key=lambda x: -x[1])

print(f"{'RICE':>8}  {'Feature':<40}  {'Reach':>8}  {'Impact':>6}  {'Conf%':>5}  {'Effort':>6}")
print("-" * 85)
for feature, rice, reach, impact, conf, effort in scored:
    print(f"{rice:>8.1f}  {feature:<40}  {reach:>8.0f}  {impact:>6.2f}  {conf:>5.0f}%  {effort:>6.1f}")
