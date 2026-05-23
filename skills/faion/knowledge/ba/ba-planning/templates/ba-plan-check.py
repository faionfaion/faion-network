#!/usr/bin/env python3
"""ba-plan-check.py — validate BA Approach Document and emit JSON status.

Checks: required frontmatter fields, valid approach value, review cadence.
Exit 0 = OK, exit 1 = errors found.

Usage: python ba-plan-check.py [ba-plan.md]
"""
from __future__ import annotations

import sys
import json
import datetime as dt
import pathlib

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required: pip install pyyaml")

REQUIRED = {"engagement_id", "approach", "version", "approver", "last_reviewed"}
APPROACHES = {"Plan-Driven", "Change-Driven", "Hybrid"}
MAX_AGE_DAYS = 14


def load_frontmatter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"{path}: missing YAML frontmatter (must start with ---)")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{path}: malformed frontmatter (missing closing ---)")
    return yaml.safe_load(parts[1]) or {}


def main(path_str: str = "ba-plan.md") -> int:
    path = pathlib.Path(path_str)
    fm = load_frontmatter(path)
    errors: list[str] = []

    missing = REQUIRED - set(fm)
    if missing:
        errors.append(f"missing required fields: {sorted(missing)}")

    if fm.get("approach") not in APPROACHES:
        errors.append(f"approach must be one of {sorted(APPROACHES)}, got: {fm.get('approach')!r}")

    age_days = None
    last = fm.get("last_reviewed")
    if isinstance(last, (dt.date, dt.datetime)):
        last_d = last if isinstance(last, dt.date) else last.date()
        age_days = (dt.date.today() - last_d).days
        if age_days > MAX_AGE_DAYS:
            errors.append(f"plan stale: {age_days}d > {MAX_AGE_DAYS}d — update last_reviewed")

    approver = fm.get("approver", "")
    if approver in ("", "name@domain", "tbd", "TBD"):
        errors.append("approver is not set to a real value; name a specific human")

    status = {
        "file": str(path),
        "errors": errors,
        "age_days": age_days,
        "ok": not errors,
    }
    print(json.dumps(status, indent=2, default=str))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "ba-plan.md"))
