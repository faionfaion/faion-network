#!/usr/bin/env python3
"""validate-user-story-mapping.py

Validate a story-map artefact (JSON) against 02-output-contract.xml.

Inputs:
    --file PATH       path to map JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid; 1 = invalid; 2 = usage / unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(r"^v\d+\.\d+\.\d+$")
BANDS = {"R1", "R2", "R3", "R4"}
GENERIC = {"features", "backlog", "todo"}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    if not SEMVER.match(obj.get("version_tag", "")):
        errs.append("version_tag must match semver pattern")
    personas = {p.get("id") for p in obj.get("personas", []) if isinstance(p, dict)}
    if not personas:
        errs.append("personas must be non-empty")
    activities = obj.get("activities", [])
    if not activities:
        errs.append("activities must be non-empty")
    if len(activities) > 8:
        errs.append(f"activities count {len(activities)} > 8 (rule r4)")
    total_stories = 0
    for i, a in enumerate(activities):
        name = (a.get("name") or "").strip().lower()
        if name in GENERIC:
            errs.append(f"activities[{i}].name '{name}' is generic (rule r1)")
        tasks = a.get("tasks", [])
        if not tasks:
            errs.append(f"activities[{i}].tasks empty")
        r1_present = False
        for j, t in enumerate(tasks):
            stories = t.get("stories", [])
            for k, s in enumerate(stories):
                total_stories += 1
                pid = s.get("persona_id")
                if not pid or pid == "all":
                    errs.append(f"stories[{i}/{j}/{k}].persona_id missing or 'all' (rule r2)")
                elif pid not in personas:
                    errs.append(f"stories[{i}/{j}/{k}].persona_id '{pid}' not in personas (rule r2)")
                if s.get("release") not in BANDS:
                    errs.append(f"stories[{i}/{j}/{k}].release '{s.get('release')}' not in {sorted(BANDS)} (rule r5)")
                if s.get("release") == "R1":
                    r1_present = True
        if not r1_present:
            errs.append(f"activities[{i}] '{a.get('id')}' lacks R1 story (rule r1)")
    if total_stories > 200:
        errs.append(f"total stories {total_stories} > 200 (rule r4 — split map)")
    return errs


OK_FIXTURE = {
    "map_id": "x", "version_tag": "v1.0.0",
    "personas": [{"id": "u", "name": "User"}],
    "activities": [
        {"id": "a1", "name": "Discover", "tasks": [{"id": "t1", "stories": [{"id": "s1", "title": "x", "persona_id": "u", "release": "R1"}]}]},
        {"id": "a2", "name": "Pay", "tasks": [{"id": "t2", "stories": [{"id": "s2", "title": "y", "persona_id": "u", "release": "R1"}]}]},
    ],
}
BAD_FIXTURE = {
    "map_id": "x", "version_tag": "latest",
    "personas": [], "activities": [{"id": "a1", "name": "Features", "tasks": []}],
}


def self_test() -> int:
    if validate(OK_FIXTURE):
        sys.stderr.write("OK rejected\n"); return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("BAD accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
