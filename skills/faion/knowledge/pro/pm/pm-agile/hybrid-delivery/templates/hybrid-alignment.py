#!/usr/bin/env python3
"""
purpose: Reference script aligning component method assignment with risk profile.
consumes: see content/02-output-contract.xml inputs for hybrid-delivery
produces: decision-record
depends-on: content/01-core-rules.xml + content/02-output-contract.xml
token-budget-impact: ~200-1000 tokens when loaded as context
"""


"""hybrid-alignment.py — flag epics misaligned with their milestone from program.yaml.

Usage: python hybrid-alignment.py program.yaml
Input: YAML with milestones[]{id, due, epics[]{id, issues_done, issues_total, team}}
Exit 0 = aligned, exit 1 = issues found (written to stderr).
"""
from __future__ import annotations
import datetime as dt
import pathlib
import sys
import yaml


def main(path: str = "program.yaml") -> int:
    program = yaml.safe_load(pathlib.Path(path).read_text())
    today = dt.date.today()
    issues: list[str] = []
    for m in program.get("milestones", []):
        due = dt.date.fromisoformat(str(m["due"]))
        days_left = (due - today).days
        for epic in m.get("epics", []):
            done = epic.get("issues_done", 0)
            total = max(epic.get("issues_total", 0), 1)
            pct = done / total
            label = f"{m['id']}/{epic['id']}"
            if days_left < 0 and pct < 1:
                issues.append(f"{label}: PAST_DUE ({-days_left}d overdue, {pct:.0%} complete)")
            elif days_left < 14 and pct < 0.5:
                issues.append(f"{label}: AT_RISK ({days_left}d left, {pct:.0%} complete)")
            elif not epic.get("team"):
                issues.append(f"{label}: ORPHAN (no team assigned)")
    if issues:
        sys.stderr.write("\n".join(issues) + "\n")
        return 1
    print("All epics aligned with milestones.")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
