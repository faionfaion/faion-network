#!/usr/bin/env python3
# purpose: verify the 5 BABOK KA1 artifacts are present and within review cadence
# consumes: directory containing T1-*.md through T5-*.md files with YAML frontmatter
# produces: JSON report listing tasks_found, tasks_missing, errors, ok flag
# depends-on: content/01-core-rules.xml (cadence rule), content/02-output-contract.xml
# token-budget-impact: ~200 tokens when loaded as context
"""ka1_check.py — verify the 5 BABOK KA1 artifacts are present and within review cadence.
Usage: python ka1_check.py <directory with T1-T5 markdown files>
"""
from __future__ import annotations

import sys
import json
import datetime as dt
import pathlib

try:
    import yaml
except ImportError:
    print(json.dumps({"error": "pyyaml not installed: pip install pyyaml"}))
    sys.exit(2)

TASKS = {
    "T1": "plan_ba_approach",
    "T2": "plan_stakeholder_engagement",
    "T3": "plan_ba_governance",
    "T4": "plan_ba_information_management",
    "T5": "identify_ba_performance_improvements",
}
REQUIRED_FIELDS = {"task_id", "version", "approver", "last_reviewed", "baselined"}
CADENCE_DAYS = {"T1": 30, "T2": 14, "T3": 30, "T4": 30, "T5": 7}


def load_frontmatter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing YAML frontmatter (must start with ---)")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{path}: malformed frontmatter")
    return yaml.safe_load(parts[1]) or {}


def main(root_str: str) -> int:
    root = pathlib.Path(root_str)
    errors: list[str] = []
    found: dict[str, dict] = {}

    for tid, slug in TASKS.items():
        candidates = list(root.glob(f"{tid}-*.md"))
        if not candidates:
            errors.append(f"{tid} ({slug}): no artifact found (expected {tid}-*.md)")
            continue

        fm = load_frontmatter(candidates[0])
        missing = REQUIRED_FIELDS - set(fm)
        if missing:
            errors.append(f"{tid}: missing frontmatter fields: {sorted(missing)}")

        approver = fm.get("approver", "")
        if not approver or approver in {"leadership", "management", "product team"}:
            errors.append(f"{tid}: approver must be a named person, got: '{approver}'")

        last = fm.get("last_reviewed")
        if isinstance(last, (dt.date, dt.datetime)):
            last_d = last if isinstance(last, dt.date) else last.date()
            age = (dt.date.today() - last_d).days
            if age > CADENCE_DAYS[tid]:
                errors.append(
                    f"{tid} stale: last_reviewed={last_d}, age={age}d > cadence={CADENCE_DAYS[tid]}d"
                )
        elif last is not None:
            errors.append(f"{tid}: last_reviewed is not a date: {last!r}")

        found[tid] = fm

    result = {
        "ok": not errors,
        "tasks_found": sorted(found),
        "tasks_missing": [t for t in TASKS if t not in found],
        "errors": errors,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
