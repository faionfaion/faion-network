#!/usr/bin/env python3
"""parse-plan.py — extract task list and dependency graph from implementation-plan.md.

Usage:
    python parse-plan.py implementation-plan.md
    python parse-plan.py implementation-plan.md --graph    # output DOT format
    python parse-plan.py implementation-plan.md --waves    # print wave groupings
"""

import re
import sys
from collections import defaultdict, deque


def parse_tasks(path: str) -> dict:
    """Return dict of task_id -> {title, depends_on, blocks, tokens, complexity}."""
    with open(path) as f:
        content = f.read()

    tasks = {}
    # Match ### TASK-NNN: Title blocks
    task_blocks = re.split(r"\n(?=### TASK-)", content)
    for block in task_blocks:
        m = re.match(r"### (TASK-\d+): (.+)", block)
        if not m:
            continue
        tid = m.group(1)
        title = m.group(2).strip()

        deps_m = re.search(r"\*\*Depends on:\*\* (.+)", block)
        blocks_m = re.search(r"\*\*Blocks:\*\* (.+)", block)
        tokens_m = re.search(r"\*\*Tokens:\*\* (~\S+)", block)
        complexity_m = re.search(r"\*\*Complexity:\*\* (\S+)", block)

        def parse_list(text: str) -> list[str]:
            if not text or text.strip().lower() in ("none", "—", "-"):
                return []
            return [t.strip() for t in re.findall(r"TASK-\d+", text)]

        tasks[tid] = {
            "title": title,
            "depends_on": parse_list(deps_m.group(1) if deps_m else ""),
            "blocks": parse_list(blocks_m.group(1) if blocks_m else ""),
            "tokens": tokens_m.group(1) if tokens_m else "?",
            "complexity": complexity_m.group(1) if complexity_m else "?",
        }
    return tasks


def compute_waves(tasks: dict) -> list[list[str]]:
    """Topological wave grouping — returns list of waves, each a list of task IDs."""
    in_degree = {tid: len(t["depends_on"]) for tid, t in tasks.items()}
    waves = []
    remaining = set(tasks)

    while remaining:
        wave = [tid for tid in remaining if in_degree[tid] == 0]
        if not wave:
            print("ERROR: circular dependency detected", file=sys.stderr)
            sys.exit(1)
        waves.append(sorted(wave))
        for tid in wave:
            remaining.discard(tid)
            for blocked in tasks[tid]["blocks"]:
                if blocked in in_degree:
                    in_degree[blocked] -= 1
    return waves


def to_dot(tasks: dict) -> str:
    lines = ["digraph tasks {", '  rankdir=LR;', '  node [shape=box];']
    for tid, t in tasks.items():
        label = f"{tid}\\n{t['tokens']}"
        lines.append(f'  "{tid}" [label="{label}"];')
    for tid, t in tasks.items():
        for dep in t["depends_on"]:
            lines.append(f'  "{dep}" -> "{tid}";')
    lines.append("}")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    path = args[0]
    show_graph = "--graph" in args
    show_waves = "--waves" in args

    tasks = parse_tasks(path)
    if not tasks:
        print("No tasks found. Check ### TASK-NNN: heading format.", file=sys.stderr)
        sys.exit(1)

    if show_graph:
        print(to_dot(tasks))
        return

    waves = compute_waves(tasks)

    if show_waves:
        for i, wave in enumerate(waves, 1):
            ids = ", ".join(wave)
            print(f"Wave {i}: {ids}")
        return

    # Default: task summary table
    print(f"{'ID':<12} {'Complexity':<12} {'Tokens':<8} {'Depends On'}")
    print("-" * 60)
    for tid, t in sorted(tasks.items()):
        deps = ", ".join(t["depends_on"]) if t["depends_on"] else "None"
        print(f"{tid:<12} {t['complexity']:<12} {t['tokens']:<8} {deps}")


if __name__ == "__main__":
    main()
