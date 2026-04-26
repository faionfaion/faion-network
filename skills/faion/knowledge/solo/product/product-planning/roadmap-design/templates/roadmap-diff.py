#!/usr/bin/env python3
"""roadmap_diff.py — diff two roadmap JSON snapshots for monthly review.

Usage: python roadmap_diff.py prev.json curr.json

Input JSON schema (each file):
{
  "now": [{"id": str, "theme": str, "confidence": str}, ...],
  "next": [{"id": str, "theme": str, "confidence": str}, ...],
  "later": [{"id": str}, ...]
}

Output (stdout): {"moved": {id: [prev_bucket, curr_bucket]}, "added": [id], "dropped": [id]}
"""
import json
import sys


def index_roadmap(rm: dict) -> dict[str, str]:
    result: dict[str, str] = {}
    for bucket in ("now", "next", "later"):
        for item in rm.get(bucket, []):
            result[item["id"]] = bucket
    return result


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: roadmap_diff.py prev.json curr.json", file=sys.stderr)
        sys.exit(2)

    prev = json.load(open(sys.argv[1]))
    curr = json.load(open(sys.argv[2]))

    p, c = index_roadmap(prev), index_roadmap(curr)
    moved = {k: [p[k], c[k]] for k in c if k in p and p[k] != c[k]}
    added = [k for k in c if k not in p]
    dropped = [k for k in p if k not in c]

    print(json.dumps({"moved": moved, "added": added, "dropped": dropped}, indent=2))


if __name__ == "__main__":
    main()
