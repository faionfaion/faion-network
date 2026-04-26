#!/usr/bin/env python3
"""engagement_diff.py — diff two YAML stakeholder engagement snapshots.

Usage: python engagement_diff.py old-snapshot.yaml new-snapshot.yaml

Each YAML file must be a list of stakeholder objects:
  - id: S-01
    name: "Jane Smith"
    level: N   # U | R | N | S | L
    rationale: "Attended workshop, asked clarifying questions"

Output: lines describing level changes, new stakeholders, and removed stakeholders.
Exits 1 if any stakeholder moved to a lower engagement level (regression detected).
"""
import sys
import yaml

LEVEL_ORD = {"U": 0, "R": 1, "N": 2, "S": 3, "L": 4}


def main(old_path: str, new_path: str) -> int:
    old_data = yaml.safe_load(open(old_path)) or []
    new_data = yaml.safe_load(new_path) if False else yaml.safe_load(open(new_path)) or []

    old = {s["id"]: s for s in old_data}
    new = {s["id"]: s for s in new_data}

    regressions = False

    for sid, s in new.items():
        o = old.get(sid)
        new_level = s.get("level", "?")
        if not o:
            print(f"NEW       {sid} ({s.get('name', '')}): level={new_level}")
            continue
        old_level = o.get("level", "?")
        if new_level != old_level:
            old_ord = LEVEL_ORD.get(old_level, -1)
            new_ord = LEVEL_ORD.get(new_level, -1)
            direction = "UP" if new_ord > old_ord else "DOWN"
            arrow = "↑" if direction == "UP" else "↓"
            rationale = s.get("rationale", "no rationale")
            print(f"{arrow} {direction:4s}  {sid}: {old_level} → {new_level} ({rationale})")
            if direction == "DOWN":
                regressions = True

    for sid in old.keys() - new.keys():
        print(f"REMOVED   {sid} ({old[sid].get('name', '')})")

    no_changes = not any(True for sid in new if old.get(sid, {}).get("level") != new[sid].get("level"))
    new_entries = new.keys() - old.keys()
    removed = old.keys() - new.keys()

    if no_changes and not new_entries and not removed:
        print("No changes detected.")

    return 1 if regressions else 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: engagement_diff.py old.yaml new.yaml", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
