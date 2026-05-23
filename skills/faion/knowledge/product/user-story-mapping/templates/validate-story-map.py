#!/usr/bin/env python3
"""validate-story-map.py — verify backbone coverage and walking-skeleton completeness.

Input:  story-map YAML file with keys:
  backbone: [{id, name, order}]
  tasks: [{id, backbone_id, name, story, acceptance:[], priority:int}]
  slices: [{name, theme, task_ids:[], value_statement}]
Output: FAIL lines per violation, exits 1 if any found.
"""
import sys
import yaml
import collections


def validate(path: str) -> list[str]:
    with open(path) as f:
        m = yaml.safe_load(f)

    errs = []
    bb = m.get("backbone", [])

    if not (5 <= len(bb) <= 10):
        errs.append(f"backbone size {len(bb)} not in 5..10")

    bb_ids = {b["id"] for b in bb}
    by_bb: dict = collections.defaultdict(list)

    for t in m.get("tasks", []):
        if t["backbone_id"] not in bb_ids:
            errs.append(f"task {t['id']} -> unknown backbone {t['backbone_id']}")
        by_bb[t["backbone_id"]].append(t)

    skeleton = next(
        (s for s in m.get("slices", []) if s["name"] == "walking_skeleton"), None
    )
    if not skeleton:
        errs.append("missing walking_skeleton slice")
    else:
        if not skeleton.get("value_statement"):
            errs.append("walking_skeleton missing value_statement")
        covered = {
            t["backbone_id"]
            for tid in skeleton["task_ids"]
            for t in m["tasks"]
            if t["id"] == tid
        }
        missing = bb_ids - covered
        if missing:
            errs.append(f"walking_skeleton missing backbone columns: {missing}")

    for bid, tasks in by_bb.items():
        if len(tasks) > 5:
            errs.append(
                f"backbone {bid} has {len(tasks)} tasks (>5); consider splitting the activity"
            )

    return errs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate-story-map.py <story-map.yaml>")
        sys.exit(2)

    errors = validate(sys.argv[1])
    for e in errors:
        print("FAIL:", e)
    sys.exit(1 if errors else 0)
