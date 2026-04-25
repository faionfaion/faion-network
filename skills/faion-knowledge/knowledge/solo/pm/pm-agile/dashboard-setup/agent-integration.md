# Agent Integration — Dashboard Setup

## When to use
- Setting up automated sprint or weekly status dashboards that pull from one or more PM tools and push to Slack/email on a schedule.
- When native PM tool dashboards (Jira gadgets, Linear Insights, ClickUp widgets) cover only part of your reporting need and you need to aggregate or transform data further.
- When stakeholders need a dashboard that combines PM metrics with deployment, incident, or business data from external systems.
- When a team is migrating PM tools and needs a neutral reporting layer that can query both old and new tools during transition.
- Onboarding a new project: use this methodology to define what metrics matter before picking widgets.

## When NOT to use
- Teams of 1–3 people with a single PM tool — native built-in dashboards are sufficient and incur no maintenance cost.
- When the bottleneck is not reporting but process: a dashboard showing a broken sprint every week is not the fix.
- Real-time alerting (P0 incidents, deploys) — PM dashboards are not low-latency enough; use PagerDuty or Grafana alerting instead.
- When the PM data is too dirty (inconsistent statuses, missing fields) to produce meaningful numbers — fix the process first.

## Where it fails / limitations
- Dashboard "freshness" depends on polling interval; a 15-minute refresh means the board can show stale data during fast-moving incidents.
- Cross-tool joins (Jira sprint + GitHub deploys + PagerDuty incidents) require a shared key (issue number or release tag) that must exist in all systems — if it is missing, joins silently drop rows.
- Jira gadgets are not configurable via REST API — gadget layout and configuration must be done manually through the UI after agent creates the dashboard.
- ClickUp widgets and Linear Insights do not export raw data via API; agents must query the underlying tasks API and compute metrics themselves.
- PowerBI dataset refresh via REST API requires a Premium workspace for scheduled refresh of push datasets — not available on free tiers.
- Report recipients quickly develop "dashboard blindness" if the signal-to-noise ratio is poor; more widgets do not mean better visibility.

## Agentic workflow
A Claude subagent can serve as a multi-tool reporting pipeline: it queries each PM tool's API on a defined schedule (daily for standups, weekly for status reports), computes normalized metrics (completion %, cycle time, blocked count), renders a structured markdown or Slack Block Kit report, and delivers it to the correct channel. For BI integration, the agent can upsert computed metrics into a Postgres table, which Grafana or Metabase then visualizes without further agent involvement. The agent should validate data completeness before rendering — if a required metric returns zero results, it should flag a data quality error rather than silently show 0%.

### Recommended subagents
- `dashboard-builder-agent` — given a PM tool config and metric spec, scaffolds the dashboard widget layout (YAML config for ClickUp, Grafana JSON, or a Slack Block Kit template) and outputs a setup checklist.
- `multi-tool-reporter` — queries Jira + Linear + GitHub on schedule, merges metrics into a unified status table, posts to Slack, archives the report as a Notion page or GitHub issue.
- `etl-pm-agent` — nightly: fetches incremental PM data from configured sources, validates schema, upserts to Postgres, triggers a Metabase/Grafana dataset refresh.

### Prompt pattern
```
Query <PM_TOOL> API for sprint <SPRINT_ID>:
- Count items by Status (Done, In Progress, Blocked, Backlog)
- Sum story points by Status
- List items where Status = Blocked (id, title, assignee)
Return JSON: {by_status: {...}, blocked_items: [...]}
Fail with error JSON if any query returns null or 0 results unexpectedly.
```

```
Given sprint metrics JSON: <metrics>
and stakeholder list: <stakeholders>
Render a Weekly Status Report per templates.md format.
Compute overall status: On Track (>=85% complete), At Risk (70-84%), Off Track (<70%).
If blocked_items > 3, add a "Blockers Require Attention" section.
Keep executive summary under 2 sentences.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | JQL queries from terminal; export to JSON/CSV | https://github.com/ankitpokhrel/jira-cli |
| `gh api` | GraphQL queries for GitHub Projects metrics | https://cli.github.com/ |
| `linear-sdk` (Node) | Cycle metrics via Linear GraphQL | `npm install @linear/sdk` |
| `psql` / `pgcli` | Query/upsert metrics database for BI tools | OS package manager |
| `metabase-cli` (community) | Trigger Metabase question refresh via API | https://github.com/metabase/metabase |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira REST API | SaaS | Yes | JQL queries for gadget data; gadget config is UI-only. |
| Linear GraphQL API | SaaS | Yes | Insights data via cycle/issue queries; no native dashboard API. |
| ClickUp API | SaaS | Yes | Task and time-tracking queries; dashboard widgets are UI-only. |
| Metabase | OSS/SaaS | Yes | REST API for question refresh and embedding; self-hostable. |
| Grafana | OSS/SaaS | Yes | JSON API for dashboard CRUD; requires data source configured. |
| PowerBI REST API | SaaS | Partial | Dataset push and refresh; Premium required for scheduled refresh. |
| Slack API | SaaS | Yes | `chat.postMessage` with Block Kit for formatted digest delivery. |
| n8n | OSS/SaaS | Yes | Orchestrate schedule → query → transform → deliver pipeline; self-hostable. |

## Templates & scripts
See `templates.md` for the full Weekly Status Report and Sprint Report markdown templates, and the Portfolio Dashboard YAML config.

Python pipeline: query Jira, compute metrics, post to Slack:
```python
import os, requests
from datetime import date

JIRA_URL  = os.environ["JIRA_URL"]
JIRA_TOKEN = os.environ["JIRA_TOKEN"]
SLACK_HOOK = os.environ["SLACK_WEBHOOK"]
PROJECT    = os.environ["JIRA_PROJECT"]

def jql_count(jql):
    r = requests.get(
        f"{JIRA_URL}/rest/api/3/search",
        headers={"Authorization": f"Bearer {JIRA_TOKEN}"},
        params={"jql": jql, "maxResults": 0},
    )
    data = r.json()
    if "total" not in data:
        raise ValueError(f"JQL failed: {data}")
    return data["total"]

sprint = f"project = {PROJECT} AND sprint in openSprints()"
total   = jql_count(sprint)
done    = jql_count(f"{sprint} AND status = Done")
blocked = jql_count(f"{sprint} AND labels = blocked AND status != Done")

if total == 0:
    requests.post(SLACK_HOOK, json={"text": "WARNING: Sprint query returned 0 items — check data quality."})
else:
    pct    = round(done / total * 100)
    status = "On Track" if pct >= 85 else ("At Risk" if pct >= 70 else "Off Track")
    msg = (
        f"*Sprint Status ({date.today()}): {status}*\n"
        f"Committed: {total} | Done: {done} ({pct}%) | Blocked: {blocked}"
    )
    requests.post(SLACK_HOOK, json={"text": msg})
```

## Best practices
- Define the metric schema in code (or a config file) before building widgets — if the metric definition changes later, all widgets break simultaneously.
- Validate every query before scheduling: run the report manually three times with real data and confirm numbers match what humans would count by hand.
- Use idempotent upserts when writing to a metrics database — duplicate runs (e.g., cron overlap) should not create duplicate rows.
- Add a data-quality guard at the start of every reporting run: if required inputs return null or unexpectedly zero, send an alert rather than a misleading report.
- Archive every generated report (Notion page, S3 file, GitHub issue) — Slack messages disappear from channel history; dashboards must be reproducible.
- Separate dashboard setup (one-time configuration) from report generation (recurring run) — agents should be able to do both but not conflate them.

## AI-agent gotchas
- Different PM tools use different completion signals: Jira uses `status = Done`, Linear uses `completedAt != null`, ClickUp uses `status = complete` — agents must use tool-specific query syntax, not a generic abstraction.
- Slack Block Kit text blocks have a 3001-character limit; an agent generating a table with many rows must chunk or truncate — test with a realistic data size.
- JQL result counts include issues the API token cannot see (private projects) — if count mismatches the board, check token permissions.
- Scheduled agents that run at sprint boundaries (Friday EOD) may catch a "transitional" state where the sprint just closed but metrics are not yet finalized — add a 1-hour buffer or query the previous closed sprint explicitly.
- An agent that runs nightly and upserts to Postgres must handle schema drift if PM tool fields change (e.g., a new status option) — use try/except with schema validation, not silent ignore.
- Human checkpoint before delivering executive-level reports: automated numbers can be accurate but contextually misleading without a narrative that explains anomalies.

## References
- https://support.atlassian.com/jira-software-cloud/docs/create-and-customize-a-dashboard/ — Jira dashboard docs
- https://linear.app/docs/insights — Linear Insights
- https://api.slack.com/block-kit — Slack Block Kit reference
- https://www.metabase.com/docs/latest/api-documentation — Metabase REST API
- https://grafana.com/docs/grafana/latest/http_api/dashboard/ — Grafana Dashboard HTTP API
- https://learn.microsoft.com/en-us/rest/api/power-bi/ — PowerBI REST API
