#!/usr/bin/env python3
"""bulk-jql-update.py — bulk-transition Jira issues matching a JQL query.

Usage:
    JIRA_BASE=https://site.atlassian.net JIRA_USER=bot@co JIRA_TOKEN=xxx \\
    python bulk-jql-update.py "project = ABC AND status = 'Awaiting QA'" 31

Args:
    jql           JQL query (quoted)
    transition_id Jira transition ID to apply

Rate limit: throttles to 5 req/sec. Handles 429 with Retry-After.
"""
import os
import sys
import time
import requests

S = requests.Session()
S.auth = (os.environ["JIRA_USER"], os.environ["JIRA_TOKEN"])
BASE = os.environ["JIRA_BASE"]


def transition(key: str, tid: str) -> None:
    r = S.post(
        f"{BASE}/rest/api/3/issue/{key}/transitions",
        json={"transition": {"id": tid}},
    )
    if r.status_code == 429:
        wait = int(r.headers.get("Retry-After", 5))
        print(f"Rate limited. Waiting {wait}s...")
        time.sleep(wait)
        return transition(key, tid)
    r.raise_for_status()
    print(f"  Transitioned {key}")


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("Usage: bulk-jql-update.py <jql> <transition_id>")
    jql, tid = sys.argv[1], sys.argv[2]

    resp = S.get(
        f"{BASE}/rest/api/3/search",
        params={"jql": jql, "fields": "key", "maxResults": 1000,
                "validateQuery": "strict"},
    )
    resp.raise_for_status()
    data = resp.json()
    issues = data.get("issues", [])
    print(f"Found {len(issues)} issues matching JQL. Transitioning...")

    for issue in issues:
        transition(issue["key"], tid)
        time.sleep(0.2)  # 5 req/sec cap

    print("Done.")


if __name__ == "__main__":
    main()
