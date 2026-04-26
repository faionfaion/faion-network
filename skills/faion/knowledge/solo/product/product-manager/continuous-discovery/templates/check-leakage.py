#!/usr/bin/env python3
"""check-leakage.py — flag releases unlinked to a research opportunity.

Leakage = shipped features with no tagged opportunity in the research repo.
Exits 1 if leakage exceeds 30%.

Input:  JSON file with structure:
  {
    "releases": [{"id": "str", "title": "str", "opp_ids": ["opp-1"]}],
    "opps":     [{"id": "str", "label": "str"}]
  }
"""
import json
import sys


def check(path: str) -> tuple[int, int, float]:
    with open(path) as f:
        data = json.load(f)

    opp_ids = {o["id"] for o in data.get("opps", [])}
    releases = data.get("releases", [])
    unlinked = [
        r for r in releases
        if not (set(r.get("opp_ids", [])) & opp_ids)
    ]
    total = len(releases)
    ratio = len(unlinked) / total if total else 0.0
    return total, len(unlinked), ratio


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check-leakage.py <releases.json>")
        sys.exit(2)

    total, unlinked_count, ratio = check(sys.argv[1])
    print(
        f"releases={total} unlinked={unlinked_count} leakage={ratio:.0%}"
    )
    if ratio > 0.30:
        print(
            f"FAIL: leakage {ratio:.0%} exceeds 30% threshold — "
            "discovery is disconnected from delivery"
        )
        sys.exit(1)
    sys.exit(0)
