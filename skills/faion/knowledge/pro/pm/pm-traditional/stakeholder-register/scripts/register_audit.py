#!/usr/bin/env python3
"""register_audit.py — audit register completeness and evidence coverage.

Usage: python register_audit.py [stakeholders/register.yaml]

Checks:
- Required fields present (name, role, category, power, interest, owner)
- attitude +/- without evidence
- High-power stakeholder without cadence
- last_engaged older than 90 days

Exits 1 if any issues found; 0 if clean.
"""
import json
import sys
import yaml
import pathlib
from datetime import date, datetime

REQUIRED = ["name", "role", "category", "power", "interest", "owner"]
STALE_DAYS = 90


def main(path: str = "stakeholders/register.yaml") -> int:
    data = yaml.safe_load(pathlib.Path(path).read_text())
    stakeholders = data.get("stakeholders", [])
    issues = []

    today = date.today()
    for s in stakeholders:
        sid = s.get("id", "?")
        for f in REQUIRED:
            if not s.get(f):
                issues.append(f"{sid}: missing required field '{f}'")

        att = s.get("attitude", "unknown")
        if att in {"+", "-"} and not s.get("evidence"):
            issues.append(f"{sid}: attitude='{att}' without evidence")

        if s.get("power") == "H" and not s.get("cadence"):
            issues.append(f"{sid}: high-power stakeholder without cadence")

        last = s.get("last_engaged")
        if last:
            last_date = datetime.strptime(str(last), "%Y-%m-%d").date()
            delta = (today - last_date).days
            if delta > STALE_DAYS:
                issues.append(f"{sid}: last_engaged {delta} days ago (threshold {STALE_DAYS})")

    result = {"issues": issues, "count": len(issues)}
    print(json.dumps(result, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
