"""
triage-idea.py — score an idea's testability and route to experiment tier.
Input:  JSON via stdin: {reversible, min_traffic_ok, behavioral_prediction, notes}
Output: JSON: {score, tier, rationale}
Tiers: A/B (score 3), prototype-or-A/B (score 2), qual-first (score 1), irreversible-strategic (score 0)
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
