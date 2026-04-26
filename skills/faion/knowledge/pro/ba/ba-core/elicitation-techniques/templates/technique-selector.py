#!/usr/bin/env python3
"""technique_selector.py — BABOK v3 elicitation technique picker.
Usage: uv run technique_selector.py situation.json
Inputs (all required): stakeholder_count, locales, time_budget_days,
  sensitivity (low|med|high), prior_artifacts[], regulated (bool),
  goal (discover_current_state|build_consensus|validate_design|
        generate_ideas|quantify_demand|derive_integrations)
Output: JSON with picks (ranked, max 3) and rejected techniques.
"""
from __future__ import annotations
import json, sys, pathlib

TECHS = [
    ("interview",         5, {"sensitivity:high": +2, "goal:discover_current_state": +2, "stakeholder_count<=10": +1}),
    ("workshop",          3, {"goal:build_consensus": +3, "stakeholder_count>=4": +1, "locales==1": +1}),
    ("focus_group",       2, {"goal:discover_current_state": +1, "stakeholder_count>=6": +1, "sensitivity:low": +1}),
    ("observation",       4, {"goal:discover_current_state": +3, "prior_artifacts<3": +1}),
    ("survey",            2, {"stakeholder_count>=30": +3, "locales>1": +2, "goal:quantify_demand": +3}),
    ("document_analysis", 4, {"prior_artifacts>=3": +3, "regulated": +2}),
    ("prototyping",       3, {"goal:validate_design": +4, "prior_artifacts>=1": +1}),
    ("brainstorming",     2, {"goal:generate_ideas": +4, "stakeholder_count>=3": +1}),
    ("interface_analysis",3, {"goal:derive_integrations": +4, "prior_artifacts>=1": +1}),
    ("collaborative_game",2, {"goal:generate_ideas": +2, "goal:build_consensus": +1, "locales==1": +1}),
]


def features(s: dict) -> set[str]:
    f = set()
    n, loc = s["stakeholder_count"], s["locales"]
    pa = len(s.get("prior_artifacts", []))
    if n <= 10: f.add("stakeholder_count<=10")
    if n >= 4:  f.add("stakeholder_count>=4")
    if n >= 6:  f.add("stakeholder_count>=6")
    if n >= 30: f.add("stakeholder_count>=30")
    f.add("locales==1" if loc == 1 else "locales>1")
    if pa < 3:  f.add("prior_artifacts<3")
    if pa >= 1: f.add("prior_artifacts>=1")
    if pa >= 3: f.add("prior_artifacts>=3")
    f.add(f"sensitivity:{s.get('sensitivity', 'low')}")
    f.add(f"goal:{s['goal']}")
    if s.get("regulated"): f.add("regulated")
    return f


def score(situation: dict) -> list[dict]:
    fs = features(situation)
    ranked = []
    for name, base, mult in TECHS:
        s = base + sum(v for k, v in mult.items() if k in fs)
        ranked.append({"technique": name, "score": s})
    ranked.sort(key=lambda x: -x["score"])
    return ranked[:3], ranked[3:]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    sit = json.loads(pathlib.Path(sys.argv[1]).read_text())
    picks, rejected = score(sit)
    print(json.dumps({
        "picks": picks,
        "rejected": [{"technique": r["technique"], "why_not": "lower yield for this situation"} for r in rejected],
        "triangulation_pair_recommended": len(picks) >= 2,
    }, indent=2))
