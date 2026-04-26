#!/usr/bin/env python3
"""mvp_capacity.py — fail if MVP scope JSON violates capacity or structural rules.

Input (stdin): JSON output of the scoping agent.
Schema: {
  "hypothesis": str,
  "kill_criterion": str,
  "learning_goals": [str],
  "timebox_weeks": int,
  "capacity_dev_per_week": float,
  "must_have": [{"id": str, "name": str, "est_days": float}],
  "should_have": [...],
  "wont_have": [{"id": str, "reason": str}]
}
Output (stdout): {"ok": bool, "problems": [str]}
Exit: 0 if ok, 1 if problems found.
"""
import json
import sys


def main() -> None:
    doc = json.load(sys.stdin)
    must_days = sum(item["est_days"] for item in doc.get("must_have", []))
    budget = doc.get("timebox_weeks", 0) * doc.get("capacity_dev_per_week", 0) * 5 * 0.6

    problems: list[str] = []
    if must_days > budget:
        problems.append(
            f"Must-Have {must_days}d exceeds 60%-budget {budget:.1f}d"
        )
    if not doc.get("kill_criterion"):
        problems.append("Missing kill_criterion")
    if not doc.get("learning_goals"):
        problems.append("Missing learning_goals")
    if len(doc.get("must_have", [])) > 5:
        problems.append(f"Too many Musts: {len(doc['must_have'])} (max 5)")
    if len(doc.get("wont_have", [])) < 3:
        problems.append(f"Won't-Have has {len(doc.get('wont_have', []))} items (min 3)")
    if not doc.get("hypothesis"):
        problems.append("Missing hypothesis")

    print(json.dumps({"ok": not problems, "problems": problems}, indent=2))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
