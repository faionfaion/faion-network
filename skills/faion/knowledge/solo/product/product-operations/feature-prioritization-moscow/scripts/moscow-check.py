#!/usr/bin/env python3
"""
moscow-check.py — validate MoSCoW budget allocation against 60/20/20 targets.

Usage:
  echo '[{"id":"auth","category":"M","effort_days":10},{"id":"pdf","category":"S","effort_days":3}]' | python moscow-check.py

Input JSON: array of {id, category (M|S|C|W), effort_days}
Output JSON: {by_cat, percentages, total_in_scope, violations}

Exit codes:
  0 — no violations
  1 — budget violations found (stderr shows details)

Tolerances:
  Must: target 60%, violation if >70% or <50%
  Should: target 20%, violation if >30%
  Could: target 20%, violation if >30%
  Won't: not counted in capacity (informational only)
"""
import json
import sys

TARGET = {"M": 0.60, "S": 0.20, "C": 0.20}
TOLERANCE = 0.10  # +/- 10% before flagging a violation


def main():
    try:
        rows = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        sys.exit(f"JSON parse error: {e}")

    valid_cats = {"M", "S", "C", "W"}
    for row in rows:
        if row.get("category") not in valid_cats:
            sys.exit(f"Invalid category '{row.get('category')}' for id '{row.get('id')}'")

    by_cat = {"M": 0, "S": 0, "C": 0, "W": 0}
    for row in rows:
        by_cat[row["category"]] += row.get("effort_days", 0)

    total_in_scope = by_cat["M"] + by_cat["S"] + by_cat["C"]
    if total_in_scope == 0:
        sys.exit("No in-scope items (M/S/C) found — cannot compute percentages")

    percentages = {
        cat: round(by_cat[cat] / total_in_scope, 3)
        for cat in ("M", "S", "C")
    }
    percentages["W"] = 0  # Won't not counted in capacity

    violations = []
    for cat, target in TARGET.items():
        actual = percentages[cat]
        if actual > target + TOLERANCE:
            violations.append(
                f"{cat} over-allocated: {actual:.0%} (target {target:.0%}, max {target + TOLERANCE:.0%})"
            )
        if cat == "M" and actual < target - TOLERANCE:
            violations.append(
                f"Must under-allocated: {actual:.0%} (target {target:.0%}, min {target - TOLERANCE:.0%})"
            )

    # Check Won't Have has entries
    w_count = sum(1 for r in rows if r.get("category") == "W")
    if w_count < 3:
        violations.append(f"Won't Have has {w_count} items (minimum required: 3)")

    result = {
        "by_cat": by_cat,
        "percentages": {k: f"{v:.0%}" for k, v in percentages.items()},
        "total_in_scope_days": total_in_scope,
        "wont_have_count": w_count,
        "violations": violations,
    }

    json.dump(result, sys.stdout, indent=2)
    print()

    if violations:
        print("\nViolations found:", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
