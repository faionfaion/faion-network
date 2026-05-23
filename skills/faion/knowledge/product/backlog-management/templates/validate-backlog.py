#!/usr/bin/env python3
"""validate-backlog.py — check ready items for DEEP/INVEST compliance and stale ratio.

Input:  backlog YAML file with key:
  items: [{id, title, type, story, acceptance:[{given,when,then}],
           size, priority, ready:bool, blockers:[], days_since_activity:int}]
Output: FAIL lines per violation, exits 1 if any found.
"""
import sys
import yaml


def validate(path: str) -> list[str]:
    with open(path) as f:
        b = yaml.safe_load(f)

    items = b.get("items", [])
    errs: list[str] = []
    ready = [i for i in items if i.get("ready")]

    for i in ready:
        iid = i.get("id", i.get("title", "?"))
        if not i.get("acceptance"):
            errs.append(f"{iid}: ready but has no acceptance criteria")
        if not i.get("size"):
            errs.append(f"{iid}: ready but has no size estimate")
        if i.get("blockers"):
            errs.append(f"{iid}: ready but has open blockers")
        story = i.get("story", "")
        if not all(kw in story for kw in ("As a", "I want", "so that")):
            errs.append(f"{iid}: story missing As-a/I-want/so-that shape")
        valid_types = {"feature", "bug", "tech_debt", "research"}
        if i.get("type") not in valid_types:
            errs.append(f"{iid}: type must be one of {valid_types}")

    if len(ready) < 8 or len(ready) > 25:
        errs.append(
            f"ready bucket size {len(ready)} is outside healthy range 8..25"
        )

    stale = [i for i in items if i.get("days_since_activity", 0) > 180
             and i.get("priority") != "p1"]
    if items:
        stale_ratio = len(stale) / len(items)
        if stale_ratio > 0.10:
            errs.append(
                f"stale ratio {stale_ratio:.0%} exceeds 10% threshold "
                f"({len(stale)} of {len(items)} items)"
            )

    return errs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate-backlog.py <backlog.yaml>")
        sys.exit(2)

    errors = validate(sys.argv[1])
    for e in errors:
        print("FAIL:", e)
    sys.exit(1 if errors else 0)
