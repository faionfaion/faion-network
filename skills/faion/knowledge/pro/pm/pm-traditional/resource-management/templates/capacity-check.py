"""capacity_check.py — flag overloaded resources per ISO week.

Usage:
  python capacity_check.py resources/roster.yaml resources/allocations.yaml
  python capacity_check.py resources/roster.yaml resources/allocations.yaml 0.75

roster.yaml shape:
  resources:
    - id: alice
      name: Alice Chen
      hours_per_week: 40

allocations.yaml shape:
  allocations:
    - resource_id: alice
      weeks:
        "2026-W17": 38
        "2026-W18": 42

Exit 0 = all within threshold, exit 1 = overloads found.
"""

import sys
from collections import defaultdict

import yaml
import pathlib


def main(roster_path: str, alloc_path: str, threshold: float = 0.85) -> int:
    roster = {
        r["id"]: r
        for r in yaml.safe_load(pathlib.Path(roster_path).read_text())["resources"]
    }
    allocations = yaml.safe_load(pathlib.Path(alloc_path).read_text())["allocations"]

    load: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for alloc in allocations:
        for week, hours in alloc["weeks"].items():
            load[alloc["resource_id"]][week] += hours

    over: list[tuple[str, str, str, float]] = []
    for rid, weeks in load.items():
        if rid not in roster:
            continue
        capacity = roster[rid]["hours_per_week"]
        for week, hours in weeks.items():
            ratio = hours / capacity
            if ratio > threshold:
                over.append((rid, roster[rid]["name"], week, ratio))

    for rid, name, week, ratio in sorted(over, key=lambda x: (-x[3], x[2])):
        sys.stdout.write(f"OVERLOAD  {rid:<12}  {name:<25}  {week}  {ratio*100:.0f}%\n")

    if over:
        sys.stderr.write(f"\n{len(over)} overload(s) found (threshold {threshold*100:.0f}%)\n")
        return 1
    sys.stdout.write("All resources within capacity threshold.\n")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        sys.stderr.write("Usage: capacity_check.py <roster.yaml> <allocations.yaml> [threshold]\n")
        sys.exit(2)
    threshold = float(args[2]) if len(args) > 2 else 0.85
    sys.exit(main(args[0], args[1], threshold))
