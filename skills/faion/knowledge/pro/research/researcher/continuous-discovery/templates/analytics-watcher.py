# purpose: Daily watcher: PostHog + tickets -> insight-log.md
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1500 tokens when loaded as context
# analytics-watcher.py — daily analytics watcher (Agent SDK pattern)
# Input: PostHog export + support ticket list since last run
# Output: appends one InsightLogEntry to .aidocs/product_docs/discovery/insight-log.md
# Schedule: cron 0 7 * * * (daily at 07:00)
from __future__ import annotations
from datetime import datetime, timedelta
from pydantic import BaseModel
from anthropic import Anthropic


class InsightLogEntry(BaseModel):
    date: str
    source: str
    user_segment: str
    observation: str
    frequency: int        # number of occurrences in the window
    severity: int         # 1-5
    ost_node_id: str | None = None  # link to OST opportunity if known


def fetch_posthog(since: str) -> dict:
    """Stub: replace with real PostHog API call."""
    return {"events": [], "since": since}


def fetch_tickets(since: str) -> list:
    """Stub: replace with real Intercom/Zendesk/Linear API call."""
    return []


def append_insight_log(entry: InsightLogEntry) -> None:
    path = ".aidocs/product_docs/discovery/insight-log.md"
    line = (
        f"\n## {entry.date}\n"
        f"- **Source:** {entry.source} | **Segment:** {entry.user_segment}\n"
        f"- **Observation:** {entry.observation}\n"
        f"- **Frequency:** {entry.frequency} | **Severity:** {entry.severity}/5\n"
        + (f"- **OST node:** {entry.ost_node_id}\n" if entry.ost_node_id else "")
    )
    with open(path, "a") as f:
        f.write(line)


def run() -> None:
    since = (datetime.utcnow() - timedelta(hours=24)).isoformat() + "Z"
    posthog_data = fetch_posthog(since)
    tickets = fetch_tickets(since)

    client = Anthropic()
    prompt = (
        f"You are the analytics-watcher (Continuous Discovery, Torres).\n"
        f"Summarize signals since {since}. Tag by OST node id if recognizable.\n"
        f"PostHog: {posthog_data}\nTickets: {tickets}\n"
        f"Return JSON matching InsightLogEntry schema. Severity 1-5. N>=5 required for any finding."
    )
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    import json
    data = json.loads(msg.content[0].text)
    entry = InsightLogEntry(**data)
    append_insight_log(entry)
    print(f"Logged insight: {entry.observation[:60]}")


if __name__ == "__main__":
    run()
