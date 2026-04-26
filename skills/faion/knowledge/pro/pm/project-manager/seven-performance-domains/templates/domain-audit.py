#!/usr/bin/env python3
"""Walk PMBoK 8 domains against a project root directory; emit JSON gap matrix.

Usage: domain-audit.py [project-root]
Default project-root: current directory.
Exit 0 always — review the JSON output; callers interpret status.
"""
import json
import os
import sys
from datetime import datetime

DOMAINS = [
    "Governance", "Scope", "Schedule", "Finance",
    "Stakeholders", "Resources", "Risk",
]

EXPECTED: dict[str, list[str]] = {
    "Governance":   ["charter.md", "decision-log.md"],
    "Scope":        ["scope.md", "wbs.md"],
    "Schedule":     ["schedule.md", "milestones.md"],
    "Finance":      ["budget.md", "cost-baseline.md"],
    "Stakeholders": ["stakeholder-register.md", "comms-plan.md"],
    "Resources":    ["raci.md", "team-charter.md"],
    "Risk":         ["risk-register.md"],
}


def file_mtime(path: str) -> str:
    try:
        ts = os.path.getmtime(path)
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    except OSError:
        return "never"


def audit(root: str) -> dict:
    out: dict = {}
    for domain in DOMAINS:
        items = []
        for fname in EXPECTED[domain]:
            fpath = os.path.join(root, fname)
            exists = os.path.isfile(fpath)
            items.append({
                "file": fname,
                "exists": exists,
                "last_updated": file_mtime(fpath) if exists else "never",
            })
        present = sum(1 for i in items if i["exists"])
        total = len(items)
        if present == total:
            status = "green"
        elif present > 0:
            status = "amber"
        else:
            status = "red"
        out[domain] = {
            "status": status,
            "items": items,
            "next_action": (
                "No action required" if status == "green"
                else f"Create missing artefact(s): "
                     + ", ".join(i["file"] for i in items if not i["exists"])
            ),
        }
    return out


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(audit(root), indent=2))
