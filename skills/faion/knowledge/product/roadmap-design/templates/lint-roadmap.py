"""
lint-roadmap.py — Validate an internal product roadmap YAML file.

Usage: python lint-roadmap.py roadmap.yaml
Exit 0 if all checks pass; exit 1 on any failure.

Expected YAML shape:
  vision: "..."
  objectives: [...]
  themes: [...]
  horizons:
    now: [{id, theme, objective_id, confidence, effort, owner, measure, status}]
    next: [...]
    later: [...]
  not_doing: [{item, reason}]
"""
import sys

import yaml

REQUIRED_KEYS = {"vision", "objectives", "themes", "horizons", "not_doing"}
MAX_NOW = 5
MAX_NEXT = 8


def lint(path: str) -> int:
    r = yaml.safe_load(open(path))
    errors = []

    missing = REQUIRED_KEYS - r.keys()
    if missing:
        errors.append(f"missing top-level keys: {missing}")

    now = r.get("horizons", {}).get("now", [])
    if len(now) > MAX_NOW:
        errors.append(f"too many initiatives in Now: {len(now)} > {MAX_NOW}")

    next_ = r.get("horizons", {}).get("next", [])
    if len(next_) > MAX_NEXT:
        errors.append(f"too many initiatives in Next: {len(next_)} > {MAX_NEXT}")

    if not r.get("not_doing"):
        errors.append("not_doing list is empty — explicit exclusions are required")

    for horizon in ("now", "next"):
        for initiative in r.get("horizons", {}).get(horizon, []):
            iid = initiative.get("id", "?")
            if "confidence" not in initiative:
                errors.append(f"{horizon}/{iid}: missing confidence field")
            if "objective_id" not in initiative:
                errors.append(f"{horizon}/{iid}: missing objective_id — orphaned initiative")
            if "measure" not in initiative:
                errors.append(f"{horizon}/{iid}: missing measure field")

    for e in errors:
        print(f"FAIL: {e}")

    if not errors:
        total = len(now) + len(next_)
        print(f"OK: roadmap passed all checks ({len(now)} in Now, {len(next_)} in Next, {total} total)")

    return 1 if errors else 0


sys.exit(lint(sys.argv[1]))
