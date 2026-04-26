#!/usr/bin/env python3
"""
Idea scoring script.
Input (stdin): JSON list of ideas, each with a "scores" object:
  {"name": "...", "scores": {"market": 4, "fit": 3, "competition": 4, "monetization": 5, "mvp": 4}}
  Note: "fit" (Personal Fit) should be scored by the founder, NOT by an LLM.
Output (stdout): JSON list of top 10 ideas sorted by weighted total.
Usage: cat ideas.json | python3 idea-scorer.py
"""
import json
import sys

WEIGHTS = {
    "market": 0.20,
    "fit": 0.25,
    "competition": 0.15,
    "monetization": 0.20,
    "mvp": 0.20,
}

ideas = json.load(sys.stdin)

for idea in ideas:
    scores = idea.get("scores", {})
    # Warn if Personal Fit was not scored (LLM should leave it blank)
    if "fit" not in scores:
        idea["weighted"] = None
        idea["note"] = "Personal Fit missing — founder must score before ranking"
        continue
    weighted = sum(WEIGHTS[k] * float(scores.get(k, 0)) for k in WEIGHTS)
    idea["weighted"] = round(weighted, 2)

ranked = sorted(
    [i for i in ideas if i.get("weighted") is not None],
    key=lambda x: x["weighted"],
    reverse=True,
)

print(json.dumps(ranked[:10], indent=2))
