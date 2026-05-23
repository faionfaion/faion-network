#!/usr/bin/env python3
"""
JTBD force aggregator.
Input (stdin): JSON list of tagged transcripts, each with a "turns" array.
  Each turn: {label: "PUSH"|"PULL"|"HABIT"|"FEAR"|"NONE", quote, severity: 1-5, interview_id}
Output (stdout): JSON summary with counts, average severities, and push_pull_vs_habit_fear score.
Positive push_pull_vs_habit_fear: market favors switching toward your solution.
Negative: inertia and fear dominate.
Usage: cat tagged_transcripts.json | python3 force-aggregator.py
"""
import json
import sys
import collections

data = json.load(sys.stdin)
agg = collections.defaultdict(list)

for transcript in data:
    for turn in transcript.get("turns", []):
        label = turn.get("label", "NONE")
        if label in {"PUSH", "PULL", "HABIT", "FEAR"}:
            agg[label].append({
                "quote": turn.get("quote", ""),
                "severity": float(turn.get("severity", 0)),
                "source": transcript.get("interview_id", "unknown"),
            })

summary = {}
for force, items in agg.items():
    summary[force] = {
        "count": len(items),
        "avg_severity": round(sum(x["severity"] for x in items) / len(items), 2) if items else 0,
        "top_quotes": [x["quote"][:150] for x in sorted(items, key=lambda x: x["severity"], reverse=True)[:3]],
    }

push_pull_total = sum(x["severity"] for x in agg.get("PUSH", []) + agg.get("PULL", []))
habit_fear_total = sum(x["severity"] for x in agg.get("HABIT", []) + agg.get("FEAR", []))
summary["push_pull_vs_habit_fear"] = round(push_pull_total - habit_fear_total, 2)
summary["interpretation"] = (
    "Switching favored" if summary["push_pull_vs_habit_fear"] > 0 else "Inertia/fear dominates"
)

print(json.dumps(summary, indent=2))
