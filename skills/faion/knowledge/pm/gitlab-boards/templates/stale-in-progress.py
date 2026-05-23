#!/usr/bin/env python3
"""stale_in_progress.py — flag issues idle in workflow::in-progress beyond N days.

Usage:  python stale_in_progress.py <project_id> [days=14]
Env:    GITLAB_URL, GITLAB_TOKEN
Exit:   1 if stale issues found (wire to CI failure → triage issue).
"""
from __future__ import annotations
import os
import sys
from datetime import datetime, timedelta, timezone
import gitlab


def main(project_id: str, days: int = 14) -> int:
    gl = gitlab.Gitlab(
        os.environ["GITLAB_URL"], private_token=os.environ["GITLAB_TOKEN"]
    )
    project = gl.projects.get(project_id)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    stale = []
    for issue in project.issues.list(
        state="opened", labels="workflow::in-progress",
        iterator=True, per_page=100,
    ):
        last = datetime.fromisoformat(issue.updated_at.replace("Z", "+00:00"))
        if last < cutoff:
            age = (datetime.now(timezone.utc) - last).days
            stale.append((issue.iid, issue.title, age))
    for iid, title, age in sorted(stale, key=lambda x: -x[2]):
        print(f"!{iid:<5} {age:>3}d  {title}")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 14))
