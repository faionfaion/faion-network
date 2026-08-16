# Reporting Dashboards

## Summary

**One-sentence:** Automated PM reporting pipeline that audits data quality, fetches read-only, computes multi-metric health (completion + scope-creep + blocked), validates before sending, archives every run, then delivers to Slack or BI.

**One-paragraph:** Sprint status reports are the most common PM overhead. This methodology automates the loop while protecting against the failure mode that destroys trust: shipping a 0% completion report because the query silently failed. The seven-step pipeline (audit → schema → fetch → compute → validate → archive → deliver) splits generation from delivery; validate-before-send aborts on degraded data. Output is a Markdown/Block-Kit report + archive record + Slack/BI delivery receipt, all generated from a fixed schema checked into the repo.

**Ефективно для:**

- Weekly sprint status to leadership without manual aggregation.
- Multi-sprint trend analysis in Metabase / Grafana via PM-tool ETL.
- Daily standup digests delivered to Slack on a cron.
- Executive cross-project rollups when stakeholders lack PM-tool access.

## Applies If (ALL must hold)

- Sprint-cadence status reporting requires manual data collection from PM tools.
- Stakeholders need a consolidated view across projects.
- Same numbers are computed every week (cron-friendly).
- PM tool exposes a read-only API + token can be scoped.

## Skip If (ANY kills it)

- Team of 1-3 people where a quick manual update is faster than building automation.
- PM tool's native dashboard already covers all stakeholder needs.
- Regulated environments requiring immutable provenance without an archive layer.
- Real-time operational on-call dashboards — PM data lags minutes to hours.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PM tool read-only API token | env var | platform |
| Report schema with status enum + threshold table | JSON in repo | tech-lead |
| Slack webhook OR BI sink config | config | engineering |
| Archive store (S3 / Notion / repo path) | config | engineering |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[notion-pm]] | Notion is a frequent source for tasks; query patterns inform fetch step. |
| [[status-report-templates-by-audience]] | Audience-specific report shaping consumes this pipeline's output. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: read-only token, schema-first, multi-metric health, validate-before-send, archive-before-deliver, separate generate/deliver | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for report artefact + valid/invalid examples + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: 0% report shipped, single-metric health, secret in delivery URL, no archive | ~800 |
| `content/04-procedure.xml` | essential | 7-step procedure: audit → schema → fetch → compute → validate → archive → deliver | ~1000 |
| `content/05-examples.xml` | essential | Worked example: weekly sprint Slack digest | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `data_quality_audit` | sonnet | Per-query judgement on what counts as "fix data first". |
| `metric_computation` | haiku | Deterministic arithmetic on fetched rows. |
| `validation_gate` | haiku | Threshold checks; no creativity. |
| `narrative_compose` | sonnet | Block-Kit Slack post or BI annotation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-report.md.j2` | Markdown sprint report skeleton |
| `templates/sprint-report.md` | Markdown sprint report skeleton Generated from `templates/sprint-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/weekly-status-report.md.j2` | Weekly leadership status template |
| `templates/weekly-status-report.md` | Weekly leadership status template Generated from `templates/weekly-status-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/jira-metrics-fetcher.py` | Read-only Jira fetch reference implementation |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reporting-dashboards.py` | Validate the report artefact against 02-output-contract schema | Pre-deliver gate |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[notion-pm]]
- [[status-report-templates-by-audience]]
- [[solo-mrr-dashboard-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs — team size, data quality score, single-metric trap, archive presence, delivery channel — onto a rule from `content/01-core-rules.xml`. Walk it before every delivery; the validate-before-send branch is the cheap gate that catches the 0% report failure.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/jira-metrics-fetcher.py`

```python
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
```
