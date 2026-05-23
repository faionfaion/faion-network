"""
lint-outcomes.py — Validate an outcome roadmap YAML file.

Usage: python lint-outcomes.py roadmap.yaml
Exit 0 if all outcomes pass; exit 1 if any fail.

Expected YAML shape:
  outcomes:
    - outcome: "Reduce churn from 8% to 5% by EOQ2"
      metric: "monthly_churn_rate"
      baseline: 8.0
      target: 5.0
      timeframe: "EOQ2"
      evidence: "Analytics dashboard: ..."
"""
import re
import sys

import yaml

REQUIRED_FIELDS = {"outcome", "metric", "baseline", "target", "timeframe", "evidence"}
MOVEMENT_VERB = re.compile(r"\b(reduce|increase|decrease|raise|cut|grow|improve)\b", re.I)


def lint(path: str) -> int:
    data = yaml.safe_load(open(path))
    outcomes = data.get("outcomes", [])
    if not outcomes:
        print("FAIL: no outcomes found in file")
        return 1

    errors = 0
    for row in outcomes:
        name = row.get("outcome", "?")
        missing = REQUIRED_FIELDS - row.keys()
        if missing:
            print(f"FAIL [{name}]: missing fields: {missing}")
            errors += 1
        if not MOVEMENT_VERB.search(str(row.get("outcome", ""))):
            print(f"WARN [{name}]: outcome has no movement verb (reduce/increase/etc.)")
            errors += 1
        try:
            if float(row["target"]) == float(row["baseline"]):
                print(f"FAIL [{name}]: target equals baseline — no movement defined")
                errors += 1
        except (KeyError, TypeError, ValueError):
            pass

    if errors == 0:
        print(f"OK: {len(outcomes)} outcome(s) passed validation")
    return 1 if errors else 0


sys.exit(lint(sys.argv[1]))
