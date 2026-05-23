#!/usr/bin/env python3
"""render-ba-package.py — story-map.json -> BRD.md + RTM.csv.

Input JSON schema:
  {product, activities: [{name, goal, tasks: [{name, stories: [{
    id, persona, want, why, release, priority, ac: [{given, when, then}]
  }]}]}]}

Usage: python render-ba-package.py story-map.json output/
"""
import json
import csv
import sys
import pathlib


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit("Usage: render-ba-package.py <story-map.json> <output-dir>")

    m = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out = pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)

    brd = ["# Business Requirements Document", f"\nProduct: {m['product']}\n"]
    rtm_rows = [("req_id", "story_id", "activity", "task", "persona", "ac_count", "release")]

    for act in m["activities"]:
        brd.append(f"\n## Activity: {act['name']}\nGoal: {act['goal']}\n")
        for task in act["tasks"]:
            brd.append(f"\n### Task: {task['name']}\n")
            for s in task["stories"]:
                rid = f"REQ-{s['id']}"
                brd.append(
                    f"- **{rid}** ({s['release']}, {s['priority']}): "
                    f"As a {s['persona']}, I want {s['want']} so that {s['why']}."
                )
                for i, ac in enumerate(s.get("ac", []), 1):
                    brd.append(
                        f"  - AC{i}: Given {ac['given']}; When {ac['when']}; Then {ac['then']}."
                    )
                rtm_rows.append((
                    rid, s["id"], act["name"], task["name"],
                    s["persona"], len(s.get("ac", [])), s["release"],
                ))
                if not s.get("ac"):
                    brd.append(f"  - GAP: missing AC for {rid}")

    (out / "BRD.md").write_text("\n".join(brd))
    with (out / "RTM.csv").open("w", newline="") as f:
        csv.writer(f).writerows(rtm_rows)
    print(f"BRD + RTM written to {out}")


if __name__ == "__main__":
    main()
