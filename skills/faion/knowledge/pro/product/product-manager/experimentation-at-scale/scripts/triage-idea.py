"""
triage-idea.py — score an idea's testability and route to experiment tier.
Input:  JSON via stdin: {reversible: bool, min_traffic_ok: bool, behavioral_prediction: bool, notes: str}
Output: JSON to stdout: {score: int, tier: str, rationale: str}

Tiers:
  3 → A/B (all three conditions met)
  2 → prototype-or-A/B (two conditions met)
  1 → qual-first (one condition met)
  0 → irreversible-strategic (none met — do not A/B test)
"""
import json, sys

TIER = {
    3: "A/B",
    2: "prototype-or-A/B",
    1: "qual-first",
    0: "irreversible-strategic",
}


def triage(idea: dict) -> dict:
    score = 0
    score += 1 if idea.get("reversible") else 0
    score += 1 if idea.get("min_traffic_ok") else 0
    score += 1 if idea.get("behavioral_prediction") else 0
    return {
        "score": score,
        "tier": TIER[score],
        "rationale": idea.get("notes", ""),
    }


if __name__ == "__main__":
    idea = json.load(sys.stdin)
    json.dump(triage(idea), sys.stdout)
    print()
