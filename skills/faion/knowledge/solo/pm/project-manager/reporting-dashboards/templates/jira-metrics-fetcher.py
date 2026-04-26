"""
Fetch Jira sprint metrics and post a status digest to Slack.

Input (env vars):
  JIRA_URL        - Jira base URL (https://yourorg.atlassian.net)
  JIRA_TOKEN      - Bearer token (API token)
  SLACK_WEBHOOK   - Slack incoming webhook URL
  SPRINT_ID       - Jira sprint ID (integer)

Output:
  Posts a Slack message with sprint status.
  Exits with code 1 if data validation fails (0 committed = query error).
"""
import os
import sys
import requests

JIRA_URL = os.environ["JIRA_URL"]
JIRA_TOKEN = os.environ["JIRA_TOKEN"]
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]
SPRINT_ID = os.environ["SPRINT_ID"]


def jira_count(jql: str) -> int:
    """Return the total issue count for a JQL query (read-only)."""
    r = requests.get(
        f"{JIRA_URL}/rest/api/3/search",
        headers={"Authorization": f"Bearer {JIRA_TOKEN}"},
        params={"jql": jql, "maxResults": 0},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["total"]


def main() -> None:
    committed = jira_count(f"sprint = {SPRINT_ID}")

    # Guard: 0 committed almost always means a bad sprint ID or timing issue
    if committed == 0:
        requests.post(SLACK_WEBHOOK, json={
            "text": f"Sprint {SPRINT_ID} report: ERROR — 0 committed issues. "
                    "Check sprint ID or sprint start date."
        }, timeout=10)
        sys.exit(1)

    completed = jira_count(f"sprint = {SPRINT_ID} AND status = Done")
    blocked = jira_count(
        f"sprint = {SPRINT_ID} AND labels = blocked AND status != Done"
    )

    pct = round(completed / committed * 100)
    if pct >= 85:
        status = "On Track"
    elif pct >= 70:
        status = "At Risk"
    else:
        status = "Off Track"

    msg = (
        f"*Sprint {SPRINT_ID} Status: {status}*\n"
        f"Committed: {committed} | Completed: {completed} ({pct}%) | "
        f"Blocked: {blocked}"
    )
    requests.post(SLACK_WEBHOOK, json={"text": msg}, timeout=10)


if __name__ == "__main__":
    main()
