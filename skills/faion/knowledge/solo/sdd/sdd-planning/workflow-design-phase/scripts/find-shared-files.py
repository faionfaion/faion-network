#!/usr/bin/env python3
"""find-shared-files.py — Detect implicit task dependencies from shared file modifications.

Files touched by multiple tasks create implicit Finish-to-Start dependencies even when
no explicit dependency is declared. This script finds them.

Usage: python3 find-shared-files.py tasks/todo/
Output: JSON mapping of file path to list of task IDs that modify it (only files with 2+ tasks).

Example output:
  {
    "src/models/user.py": ["TASK-003", "TASK-007"],
    "src/middleware/auth.ts": ["TASK-002", "TASK-005", "TASK-009"]
  }
"""
import re
import sys
import json
from pathlib import Path


def find_shared_files(tasks_dir: str) -> dict[str, list[str]]:
    """Find files modified by multiple tasks — these create implicit FS dependencies."""
    file_to_tasks: dict[str, list[str]] = {}
    pattern = re.compile(r"^\|\s*(CREATE|MODIFY|DELETE)\s*\|\s*`([^`]+)`", re.MULTILINE)

    tasks_path = Path(tasks_dir)
    task_files = list(tasks_path.glob("TASK_*.md")) + list(tasks_path.glob("TASK-*.md"))

    if not task_files:
        print(f"No task files found in {tasks_dir}", file=sys.stderr)
        sys.exit(1)

    for task_file in sorted(task_files):
        task_id = task_file.stem
        text = task_file.read_text()
        for _, file_path in pattern.findall(text):
            file_to_tasks.setdefault(file_path, []).append(task_id)

    # Return only files touched by 2+ tasks
    shared = {f: tasks for f, tasks in file_to_tasks.items() if len(tasks) > 1}
    return shared


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <tasks-directory>", file=sys.stderr)
        sys.exit(1)

    shared = find_shared_files(sys.argv[1])

    if not shared:
        print("No shared files found — no implicit dependencies detected")
    else:
        print(f"Found {len(shared)} shared file(s) creating implicit FS dependencies:")
        print(json.dumps(shared, indent=2))
        print("\nAdd these as explicit Finish-to-Start dependencies in the task files.")
