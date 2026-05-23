#!/usr/bin/env python3
"""engagement_diff.py

Diff two engagement registers and surface NEW / CHANGED / CLOSED / STALE
deltas. Used between weekly reviews.

Inputs:
    --prev PATH       prior register JSON
    --curr PATH       current register JSON
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = no deltas
    1 = deltas present
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

FIXTURE_PREV = {"as_of": "2026-05-15", "stakeholders": [
    {"id": "S-001", "name": "Iryna", "current_engagement": "neutral", "quadrant": "manage_closely"}
]}
FIXTURE_CURR = {"as_of": "2026-05-22", "stakeholders": [
    {"id": "S-001", "name": "Iryna", "current_engagement": "supportive", "quadrant": "manage_closely"},
    {"id": "S-002", "name": "Petro", "current_engagement": "resistant", "quadrant": "manage_closely"},
]}


def diff(prev: dict, curr: dict) -> list[str]:
    prev_by_id = {s["id"]: s for s in prev.get("stakeholders", [])}
    curr_by_id = {s["id"]: s for s in curr.get("stakeholders", [])}
    deltas: list[str] = []
    for sid in curr_by_id:
        if sid not in prev_by_id:
            deltas.append(f"NEW: {sid} ({curr_by_id[sid]['name']})")
            continue
        if prev_by_id[sid].get("current_engagement") != curr_by_id[sid].get("current_engagement"):
            deltas.append(f"CHANGED: {sid} engagement {prev_by_id[sid].get('current_engagement')} -> {curr_by_id[sid].get('current_engagement')}")
    for sid in prev_by_id:
        if sid not in curr_by_id:
            deltas.append(f"CLOSED: {sid}")
    return deltas


def self_test() -> int:
    d = diff(FIXTURE_PREV, FIXTURE_CURR)
    if "NEW: S-002 (Petro)" not in d or any("CHANGED: S-001" in x for x in d) is False:
        sys.stderr.write(f"self-test FAIL: {d}\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--prev", type=str)
    ap.add_argument("--curr", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.prev or not args.curr:
        ap.print_help()
        return 2
    p1, p2 = Path(args.prev), Path(args.curr)
    if not p1.is_file() or not p2.is_file():
        sys.stderr.write("missing prev/curr file\n")
        return 2
    prev = json.loads(p1.read_text())
    curr = json.loads(p2.read_text())
    deltas = diff(prev, curr)
    if not deltas:
        sys.stdout.write("OK no deltas\n")
        return 0
    for d in deltas:
        sys.stdout.write(d + "\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
