# Continuous Discovery

## Summary

**One-sentence:** Teresa Torres weekly-rhythm discovery: 6-cadence pipeline (daily signals -> weekly interviews + competitor + assumption tests -> bi-weekly OST -> monthly review) with N>=5 evidence floor and 8 scheduled subagents.

**One-paragraph:** Teresa Torres' framework embedded into the weekly delivery rhythm via 8 scheduled subagents: daily signal collection (Haiku), weekly interviews/competitor monitoring/assumption testing (Sonnet), bi-weekly OST synthesis (Opus), monthly research review. Outputs land in .aidocs/product_docs/discovery/. The framework bans the word 'validated', enforces N>=5 observations across >=2 sources, and rejects solution-shaped intake.

**Ефективно для:**

- Live продукт з активними users де volume сигналів перевищує те що PM може прочитати.
- Product Trio workflow з weekly cadence customer touchpoints.
- Ринки з 6-місячним half-life на user-need validity (AI, fintech, dev tools).
- Solo операції: один operator симулює trio покриття через subagents.
- Після launch коли growth уповільнюється і треба ловити 'solution stopped working'.

## Applies If (ALL must hold)

- Live product with active users where signal volume exceeds what one PM can review unaided.
- Product Trio (PM + designer + engineer) needing a weekly cadence of customer touchpoints.
- Markets with 6-month half-life on user-need validity.
- Solopreneur stacks where one operator must simulate trio coverage via subagents.
- Post-launch slowdowns where the 6-month-ago solution no longer works.

## Skip If (ANY kills it)

- Pre-PMF zero-to-one with no users yet - start with customer-development first.
- Compliance-bound enterprise sales where contract cycles are 6-18 months.
- Hardware / regulated medical where each iteration ships in months.
- Crisis mode (active outage, churn cliff) - switch to root-cause first.
- When stakeholders demand 'validated' answers from a single interview.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Open OST | markdown / opportunity-solution-tree.md | previous discovery cycle |
| Open assumptions register | markdown | previous bi-weekly synth |
| Recurring recruit source | in-app prompt / panel / Userinterviews.com | research ops |
| Analytics + ticket sources | PostHog / Intercom / Zendesk | infrastructure |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[opportunity-solution-trees]] | consumed for the bi-weekly synthesis output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `analytics-watcher` | haiku | Mechanical daily metric pull. |
| `support-triage` | haiku | Daily ticket cluster + count + severity tagging. |
| `competitor-monitor` | haiku | Weekly RSS/changelog scrape diff. |
| `interview-synthesizer` | sonnet | Per-call transcript -> tagged notes + JTBD pulls. |
| `assumption-tester` | sonnet | Weekly test design + result rubric for OST leaves. |
| `discovery-synthesizer` | opus | Bi-weekly cross-source pattern recognition. |
| `research-reviewer` | opus | Monthly strategic memo + kill list. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost-schema.json` | OST node schema (id/type/parent/evidence/status) |
| `templates/analytics-watcher.py` | Daily watcher: PostHog + tickets -> insight-log.md |
| `templates/crontab.txt` | Cron schedule for 4 discovery cadences |
| `templates/discovery-report.md.j2` | Monthly research-review skeleton (kill list + doubled-down) |
| `templates/discovery-report.md` | Monthly research-review skeleton (kill list + doubled-down) Generated from `templates/discovery-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-continuous-discovery.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[opportunity-solution-trees]]
- [[user-research-at-scale]]
- [[persona-building]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ost-schema.json`

```json
{}
```

### `templates/analytics-watcher.py`

```python
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
```

### `templates/crontab.txt`

```text
# Continuous Discovery cron schedule
# Install: crontab -e and paste these lines
# Assumes claude CLI is at /usr/local/bin/claude

# Daily at 07:00: analytics watcher + support triage
0 7 * * *   /usr/local/bin/claude run /discovery-daily >> /var/log/discovery-daily.log 2>&1

# Weekly Monday at 08:00: interviews + competitor monitoring + assumption testing
0 8 * * 1   /usr/local/bin/claude run /discovery-weekly >> /var/log/discovery-weekly.log 2>&1

# Bi-weekly on 1st and 15th at 09:00: OST synthesis (Opus)
0 9 1,15 * * /usr/local/bin/claude run /discovery-synth >> /var/log/discovery-synth.log 2>&1

# Monthly on 1st at 10:00: research review + kill list + strategic memo
0 10 1 * *  /usr/local/bin/claude run /discovery-monthly >> /var/log/discovery-monthly.log 2>&1
```
