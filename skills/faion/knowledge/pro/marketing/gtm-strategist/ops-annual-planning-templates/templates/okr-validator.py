"""
OKR sanity check for annual and quarterly planning.

For each key result, checks:
  (a) outcome vs activity: flags verbs like "launch", "build", "ship", "publish", "create"
  (b) numeric target: must contain at least one digit
  (c) baseline and target fields: both must be present

Input:
  objective    -- string: the objective text
  key_results  -- list of dicts: [{text, current, target}, ...]

Output:
  dict with objective, issues list (per KR), and ok flag
"""


ACTIVITY_VERBS = [
    "launch", "build", "ship", "publish", "create", "develop",
    "implement", "deploy", "produce", "write", "design", "set up",
]


def validate_okr(objective: str, key_results: list[dict]) -> dict:
    issues = []

    for kr in key_results:
        text = kr.get("text", "")
        kr_issues = []

        # (a) activity vs outcome
        if any(verb in text.lower() for verb in ACTIVITY_VERBS):
            kr_issues.append(
                f"looks like an activity, not an outcome — rephrase to describe "
                f"the measurable result of the work"
            )

        # (b) numeric target
        if not any(c.isdigit() for c in text):
            kr_issues.append("no numeric target — add a number, unit, and date")

        # (c) baseline and target
        if "current" not in kr or kr.get("current") is None:
            kr_issues.append("missing baseline (current value)")
        if "target" not in kr or kr.get("target") is None:
            kr_issues.append("missing target value")

        if kr_issues:
            issues.append({
                "kr": text,
                "issues": kr_issues,
                "ok": False,
            })
        else:
            issues.append({"kr": text, "issues": [], "ok": True})

    return {
        "objective": objective,
        "key_results": issues,
        "ok": all(kr["ok"] for kr in issues),
    }


# Example:
# validate_okr(
#     "Grow recurring revenue",
#     [
#         {"text": "Launch referral program by Q2", "current": None, "target": None},
#         {"text": "Increase referral-sourced customers to 15/month by Q2",
#          "current": 0, "target": 15},
#     ],
# )
