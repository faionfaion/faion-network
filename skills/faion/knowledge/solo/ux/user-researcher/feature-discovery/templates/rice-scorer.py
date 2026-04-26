# rice_scorer.py — compute RICE scores for feature candidates
# Input:  features list with reach, impact, confidence (0-1), effort (person-weeks)
# Output: sorted table with RICE score per feature

features = [
    {"name": "Customizable dashboard", "reach": 1000, "impact": 2,   "confidence": 0.8, "effort": 3},
    {"name": "CSV export",             "reach": 500,  "impact": 1,   "confidence": 1.0, "effort": 1},
    {"name": "AI suggestions",         "reach": 800,  "impact": 3,   "confidence": 0.5, "effort": 8},
    {"name": "Dark mode",              "reach": 1200, "impact": 0.5, "confidence": 0.8, "effort": 2},
]

for f in features:
    f["rice"] = round((f["reach"] * f["impact"] * f["confidence"]) / f["effort"], 1)

print(f"{'RICE':>7}  Feature")
print("-" * 40)
for f in sorted(features, key=lambda x: -x["rice"]):
    print(f"{f['rice']:7.1f}  {f['name']}")
