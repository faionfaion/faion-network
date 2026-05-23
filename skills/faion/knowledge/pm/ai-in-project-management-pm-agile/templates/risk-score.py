#!/usr/bin/env python3
# purpose: Python helper that scores risk items Low/Medium/High from a JSON risk register; consumed by the digest pipeline.
# consumes: methodology inputs listed in AGENTS.md `## Prerequisites`
# produces: input for the artefact matching content/02-output-contract.xml
# depends-on: templates/header.yaml for frontmatter contract; AGENTS.md for body sections
# token-budget-impact: <600 tokens; validates via scripts/validate-<slug>.py

"""risk-score.py — score risk register items Low/Medium/High.
Input: risks.json — list of {id, last_updated (YYYY-MM-DD), dependent_tasks (int), owner, description}
Output: same list with added "score" field, printed as JSON.
Usage: python risk-score.py risks.json
"""
import json
import datetime
import sys


def score_risk(risk: dict) -> str:
    days_stale = (
        datetime.date.today()
        - datetime.date.fromisoformat(risk["last_updated"])
    ).days
    dep_count = risk.get("dependent_tasks", 0)
    if days_stale > 14 or dep_count > 5:
        return "High"
    if days_stale > 7 or dep_count > 2:
        return "Medium"
    return "Low"


risks = json.loads(sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read())
for r in risks:
    r["score"] = score_risk(r)
print(json.dumps(risks, indent=2))
