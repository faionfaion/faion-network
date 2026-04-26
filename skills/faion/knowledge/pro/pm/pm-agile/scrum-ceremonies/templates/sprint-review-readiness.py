#!/usr/bin/env python3
"""sprint-review-readiness.py — gate for "is this sprint ready to demo?"

Usage: python sprint-review-readiness.py sprint.json
Input JSON: {committed_points, completed_points, committed: [{status, demoable}],
             demo_environment, invited_stakeholders, escaped_bugs}
Exit 0 = ready, exit 1 = not ready (reasons printed).
"""
from __future__ import annotations
import json
import sys


def main(path: str) -> int:
    s = json.load(open(path))
    issues = []
    ratio = s["completed_points"] / max(s["committed_points"], 1)
    if ratio < 0.6:
        issues.append(f"low completion ratio ({ratio:.0%}, threshold 60%)")
    if any(i["status"] != "Done" for i in s["committed"] if i.get("demoable")):
        issues.append("undone demoable items present")
    if not s.get("demo_environment"):
        issues.append("no demo environment URL specified")
    if not s.get("invited_stakeholders"):
        issues.append("no stakeholders invited")
    if s.get("escaped_bugs", 0) > 3:
        issues.append(f"too many escaped bugs to demo cleanly ({s['escaped_bugs']})")
    if issues:
        print("NOT READY:")
        for i in issues:
            print(f"  - {i}")
        return 1
    print("Sprint review ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
