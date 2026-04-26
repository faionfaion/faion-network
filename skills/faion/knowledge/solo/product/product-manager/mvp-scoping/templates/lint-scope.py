"""
lint-scope.py — Validate an MVP scope YAML document.

Usage: python lint-scope.py scope.yaml
Exit 0 if all checks pass; exit 1 on any failure.

Expected YAML shape:
  learning_goal: "Will users track time daily?"
  kill_signal: "If <40% of users log time on 3+ days in 2 weeks, pivot"
  budget_days: 20
  features:
    - name: "Start/stop timer"
      priority: must  # must | should | could | wont
      effort_days: 3
    - name: "Mobile app"
      priority: wont
      effort_days: 0
  wont_have:
    - feature: "Mobile app"
      reason: "Responsive web is sufficient for validation"
"""
import sys

import yaml


def lint(path: str) -> int:
    doc = yaml.safe_load(open(path))
    errors = []

    musts = [f for f in doc.get("features", []) if f.get("priority") == "must"]
    if len(musts) > 5:
        errors.append(f"too many must-haves: {len(musts)} > 5 (cap is 5)")

    if not doc.get("learning_goal"):
        errors.append("missing learning_goal — define what you want to learn")

    if not doc.get("kill_signal"):
        errors.append("missing kill_signal — define the evidence that stops the project")

    if not doc.get("wont_have"):
        errors.append("missing wont_have list — explicit exclusions required")

    budget = doc.get("budget_days", 0)
    if budget > 0:
        spent = sum(
            f.get("effort_days", 0)
            for f in doc.get("features", [])
            if f.get("priority") in {"must", "should"}
        )
        if spent > budget:
            errors.append(f"effort {spent}d exceeds budget {budget}d — cut scope")

    for e in errors:
        print(f"FAIL: {e}")

    if not errors:
        print(f"OK: scope passed all checks ({len(musts)} must-haves, {budget}d budget)")

    return 1 if errors else 0


sys.exit(lint(sys.argv[1]))
