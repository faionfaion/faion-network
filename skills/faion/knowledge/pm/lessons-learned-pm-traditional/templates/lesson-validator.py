# purpose: Validator script: required fields, category in taxonomy, retrievability check
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

"""lesson_validator.py — validate a lesson dict against required schema.

Usage:
  lesson = {
      "title": "New framework without training budget",
      "category": "technical",
      "impact_level": "high",
      "situation": "Chose new framework with no team experience.",
      "impact": "Development took 40% longer than estimated.",
      "root_cause": "Training time not estimated; excitement over new tech.",
      "lesson": "New technology requires explicit ramp time.",
      "recommendation": "Add 25% buffer when introducing a framework new to the team.",
  }
  ok, msg = validate(lesson)
"""

REQUIRED = ["situation", "impact", "root_cause", "lesson", "recommendation"]
VALID_CATEGORIES = {
    "planning", "execution", "technical", "team", "vendor", "stakeholder", "other"
}
ACTION_VERBS = {
    "add", "remove", "change", "require", "reject", "schedule", "train",
    "document", "review", "escalate", "measure", "tag", "automate",
    "budget", "allocate", "enforce", "update", "introduce", "define",
}


def validate(lesson: dict) -> tuple[bool, str]:
    missing = [k for k in REQUIRED if not lesson.get(k)]
    if missing:
        return False, f"missing fields: {missing}"

    cat = lesson.get("category", "")
    if cat not in VALID_CATEGORIES:
        return False, f"category must be one of {sorted(VALID_CATEGORIES)}, got '{cat}'"

    if lesson.get("impact_level") not in ("high", "medium", "low"):
        return False, "impact_level must be high | medium | low"

    rec = lesson["recommendation"].lower()
    if not any(v in rec for v in ACTION_VERBS):
        return False, "recommendation lacks an action verb (add/remove/change/...)"

    if len(lesson["recommendation"].split()) < 6:
        return False, "recommendation too vague (< 6 words)"

    return True, "ok"
