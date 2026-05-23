#!/usr/bin/env python3
"""storymap_check.py — validate skeleton coverage and release backbone spans.

Input (stdin): JSON story map.
Schema: {
  "backbone": [str],
  "tasks": [{"activity": str, "task": str, "rank": int,
             "release": str, "walking_skeleton": bool}]
}
Output (stdout): {"ok": bool, "problems": [str]}
Exit: 0 if ok, 1 if problems found.
"""
import json
import sys


def main() -> None:
    m = json.load(sys.stdin)
    activities = set(m["backbone"])
    tasks = m.get("tasks", [])

    skeleton = [t for t in tasks if t.get("walking_skeleton")]
    skeleton_acts = {t["activity"] for t in skeleton}

    problems: list[str] = []

    missing = activities - skeleton_acts
    if missing:
        problems.append(f"Walking skeleton missing activities: {sorted(missing)}")
    if len(skeleton) != len(activities):
        problems.append(
            f"Skeleton must have exactly one task per activity "
            f"(found {len(skeleton)}, expected {len(activities)})"
        )

    by_release: dict[str, set[str]] = {}
    for t in tasks:
        rel = t.get("release")
        if rel and rel not in (None, "backlog"):
            by_release.setdefault(rel, set()).add(t["activity"])

    for r, covered in by_release.items():
        missing_in_release = activities - covered
        if missing_in_release:
            problems.append(
                f"Release '{r}' does not span all activities "
                f"(missing: {sorted(missing_in_release)})"
            )

    print(json.dumps({"ok": not problems, "problems": problems}, indent=2))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
