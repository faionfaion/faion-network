#!/usr/bin/env python3
"""Extract wave → tasks mapping from implementation-plan.md wave analysis table.

Usage: python3 extract-waves.py implementation-plan.md
Output: JSON mapping of wave number to list of task IDs.

Example:
  {"1": ["TASK-001", "TASK-002"], "2": ["TASK-003"], "3": ["TASK-004", "TASK-005"]}
"""
import re
import sys
import json


def extract_waves(path: str) -> dict[str, list[str]]:
    waves: dict[str, list[str]] = {}
    with open(path) as f:
        in_wave_table = False
        for line in f:
            if "## Wave Analysis" in line:
                in_wave_table = True
                continue
            if in_wave_table and line.startswith("##"):
                break
            if in_wave_table:
                m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+)", line)
                if m:
                    wave_num = m.group(1)
                    tasks = re.findall(r"TASK-\d+", m.group(2))
                    if tasks:
                        waves[wave_num] = tasks
    return waves


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} implementation-plan.md", file=sys.stderr)
        sys.exit(1)
    result = extract_waves(sys.argv[1])
    if not result:
        print("No wave analysis table found in file", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, indent=2))
