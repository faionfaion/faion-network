#!/usr/bin/env python3
"""Validate a risk register YAML and emit a heatmap markdown.

Input: risks.yaml with top-level key 'risks', each having:
  id, probability (VL|L|M|H|VH), impact (VL|L|M|H|VH),
  score (int), strategy (str), contingency_plan or contingency_amount (if Accept).
Output: heatmap table on stdout; exits non-zero on first violation.
"""
import sys
import yaml

LEVELS = {"VL": 1, "L": 2, "M": 3, "H": 4, "VH": 5}


def main(path):
    data = yaml.safe_load(open(path))
    risks = data["risks"]
    grid = [[[] for _ in range(5)] for _ in range(5)]
    for r in risks:
        p = LEVELS[r["probability"]] - 1
        i = LEVELS[r["impact"]] - 1
        computed = (p + 1) * (i + 1)
        if computed != r.get("score"):
            sys.exit(f"ERROR {r['id']}: score mismatch — stored {r.get('score')} computed {computed}")
        if r["strategy"] == "Accept" and not (
            r.get("contingency_amount") or r.get("contingency_plan")
        ):
            sys.exit(f"ERROR {r['id']}: Accept requires contingency_amount or contingency_plan")
        if not r.get("owner") or r["owner"].lower() in ("the team", "team", "unassigned"):
            print(f"WARN {r['id']}: owner is '{r.get('owner')}' — assign a named individual")
        grid[i][p].append(r["id"])

    opportunities = sum(1 for r in risks if r.get("is_opportunity"))
    threats = len(risks) - opportunities
    if threats >= 10 and opportunities == 0:
        print("WARN: no opportunities in register — include at least 1 per 10 threats")

    print("\n| P\\I | VL | L  | M  | H  | VH |")
    print("|-----|----|----|----|----|----|")
    level_keys = list(LEVELS.keys())
    for pi, row in enumerate(grid):
        cells = " | ".join(",".join(c) if c else "-" for c in row)
        print(f"| {level_keys[pi]}  | {cells} |")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: validate-register.py risks.yaml")
    main(sys.argv[1])
