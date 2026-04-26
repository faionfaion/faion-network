#!/usr/bin/env python3
"""bulk_jql_transition.py — bulk-transition Jira issues matching a JQL query.

Rate-limited to 5 req/s with Retry-After handling.

Usage:
    JIRA_USER=me@example.com JIRA_TOKEN=<api_token> JIRA_BASE=https://myorg.atlassian.net \\
        python3 bulk-transition.py "project = PROJ AND status = 'To Do'" "21"

Arguments:
    jql        JQL query identifying issues to transition
    tid        Transition ID (get from /rest/api/3/issue/{key}/transitions)
"""
from __future__ import annotations

import os
import sys
import time

import requests

S = requests.Session()
S.auth = (os.environ["JIRA_USER"], os.environ["JIRA_TOKEN"])
BASE = os.environ["JIRA_BASE"].rstrip("/")


def transition(key: str, tid: str) -> None:
    r = S.post(
        f"{BASE}/rest/api/3/issue/{key}/transitions",
        json={"transition": {"id": tid}},
    )
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", 5))
        time.sleep(wait)
        return transition(key, tid)
    r.raise_for_status()


def main() -> int:
    jql = sys.argv[1]
    tid = sys.argv[2]
    start_at = 0
    total_done = 0

    while True:
        r = S.get(
            f"{BASE}/rest/api/3/search",
            params={
                "jql": jql,
                "fields": "key",
                "startAt": start_at,
                "maxResults": 100,
            },
        )
        r.raise_for_status()
        data = r.json()
        issues = data["issues"]
        if not issues:
            break
        for it in issues:
            key = it["key"]
            transition(key, tid)
            total_done += 1
            print(f"  transitioned {key} ({total_done})")
            time.sleep(0.2)  # max ~5 req/s
        start_at += len(issues)
        if start_at >= data["total"]:
            break

    print(f"Done. Transitioned {total_done} issues.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
