# Agent Integration — Reporting Dashboards

## When to use
- Weekly or sprint-cadence status reporting that currently requires manual data collection from multiple PM tools.
- When stakeholders need a consolidated view across several projects (portfolio-level) without access to the underlying PM tool.
- When PM tool native reports are insufficient and data needs to be cross-referenced with external sources (time tracking, deployment logs, incident data).
- Automating digest messages to Slack/email on a fixed schedule so the team does not manually write status updates.
- When you need to feed PM data into BI tools (PowerBI, Metabase, Grafana) for trend analysis over time.

## When NOT to use
- Teams of 1–3 people where a quick manual update is faster than building dashboard automation.
- When the PM tool's native dashboard covers all stakeholder needs — adding a second layer creates maintenance burden.
- Regulated environments where report provenance and immutability must be guaranteed — automated reports lack audit trails unless you archive outputs explicitly.
- Real-time operational dashboards (e.g., incident response) — PM dashboards lag by minutes to hours and are not appropriate for live alerting.

## Where it fails / limitations
- Dashboard data is only as clean as the underlying PM data; agents surfacing stale or inconsistently labeled issues create misleading reports.
- Scheduled reports sent to Slack lose context over time — recipients stop reading them within 2–4 weeks if signal-to-noise is poor.
- PowerBI/Grafana connectors to Jira/Linear/Notion require API tokens with long expiry; token rotation breaks pipelines silently.
- JQL (Jira Query Language) results are capped at 1000 items per request; dashboards aggregating large backlogs need pagination.
- Jira gadget dashboards are per-user by default — sharing requires explicit permission configuration that admins often miss.
- Cross-tool dashboards (e.g., Jira issues + GitHub commits + PagerDuty incidents) require a data warehouse or ETL step; agents cannot JOIN data across APIs in a single pass.

## Agentic workflow
A Claude subagent can serve as a weekly report generator: it queries the PM tool API for sprint metrics (velocity, completion rate, blocked items), formats a structured markdown report, and posts it to Slack or emails it to stakeholders. For BI pipelines, an agent can run nightly to fetch updated data via REST/GraphQL, transform it to a flat schema, and upsert into a Postgres or BigQuery table that feeds a Grafana or Metabase dashboard. Report generation agents should treat data as read-only and never modify PM records during a reporting run.

### Recommended subagents
- `sprint-report-agent` — queries PM tool at sprint end, computes velocity/completion/bug metrics, renders a markdown report, posts to Slack and archives as a file.
- `portfolio-dashboard-agent` — reads status across multiple projects/boards, builds a health-status table (On Track / At Risk / Off Track), delivers to stakeholder distribution list.
- `pm-etl-agent` — nightly job: fetches incremental PM data, transforms to flat schema, upserts to a database table for BI consumption.

### Prompt pattern
```
Query <PM_TOOL> for sprint <SPRINT_ID>:
- Total issues committed vs completed (by count and story points)
- Issues still open (not Done or Cancelled)
- Issues added mid-sprint (created after sprint start date)
Return JSON: {committed, completed, incomplete, scope_added}.
Do not modify any issues.
```

```
Given this sprint metrics JSON: <metrics>
Render a Weekly Status Report in the format from templates.md:
- Status: On Track if completion >= 85%, At Risk if 70-84%, Off Track if < 70%.
- Fill all table cells; use "N/A" for missing data.
- Keep the narrative under 3 sentences.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | Query Jira via JQL from terminal, export to JSON/CSV | `brew install jira-cli` / https://github.com/ankitpokhrel/jira-cli |
| `gh` (GitHub CLI) | Fetch GitHub project items and issue stats | https://cli.github.com/ |
| `linear-sdk` (Node) | GraphQL queries against Linear for cycle metrics | `npm install @linear/sdk` |
| `notion-client` (Python) | Query Notion databases for rollup metrics | `pip install notion-client` |
| `curl` + `jq` | Universal API querying and JSON shaping for any PM tool | OS package manager |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Dashboards | SaaS | Partial | UI-only configuration; gadgets not configurable via API. |
| Linear Insights | SaaS | Partial | Built-in analytics; raw data accessible via GraphQL. |
| PowerBI | SaaS | Yes | REST API for dataset refresh; connectors to Jira/Linear via third-party. |
| Metabase | OSS/SaaS | Yes | REST API; self-hostable; good for internal PM metric dashboards. |
| Grafana | OSS/SaaS | Yes | JSON API for dashboards; requires data source (Postgres, InfluxDB, etc.). |
| n8n | OSS/SaaS | Yes | Orchestrate PM API queries → transform → post to Slack/email on schedule. |
| Slack API | SaaS | Yes | `chat.postMessage` for digest delivery; Block Kit for structured formatting. |

## Templates & scripts
See `templates.md` for full Weekly Status Report and Sprint Report markdown templates.

Python script to pull Jira sprint metrics and post to Slack:
```python
import os, requests

JIRA_URL = os.environ["JIRA_URL"]
JIRA_TOKEN = os.environ["JIRA_TOKEN"]
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]
SPRINT_ID = os.environ["SPRINT_ID"]

def jira_count(jql):
    r = requests.get(
        f"{JIRA_URL}/rest/api/3/search",
        headers={"Authorization": f"Bearer {JIRA_TOKEN}"},
        params={"jql": jql, "maxResults": 0},
    )
    return r.json()["total"]

committed = jira_count(f"sprint = {SPRINT_ID}")
completed = jira_count(f"sprint = {SPRINT_ID} AND status = Done")
blocked   = jira_count(f"sprint = {SPRINT_ID} AND labels = blocked AND status != Done")

pct = round(completed / committed * 100) if committed else 0
status = "On Track" if pct >= 85 else ("At Risk" if pct >= 70 else "Off Track")

msg = (
    f"*Sprint {SPRINT_ID} Status: {status}*\n"
    f"Committed: {committed} | Completed: {completed} ({pct}%) | Blocked: {blocked}"
)
requests.post(SLACK_WEBHOOK, json={"text": msg})
```

## Best practices
- Define a fixed report schema before automating — ad-hoc report formats confuse recipients and generate "what does this number mean?" questions.
- Add a link to the live dashboard in every automated message so recipients can drill down without asking the agent for more detail.
- Archive every generated report as a file (Notion page, S3 object, or GitHub issue comment) so there is a historical record beyond Slack scroll history.
- Validate data before sending: if `committed == 0`, the sprint query probably failed — send an error alert, not a 0% completion report.
- Use idempotent upserts when writing to a database — running the ETL agent twice should not create duplicate rows.
- Separate report delivery from report generation in your agent chain: generate → review (or auto-validate) → deliver. Skipping review leads to sending broken tables or missing data.

## AI-agent gotchas
- PM tool APIs return paginated results; an agent that stops at page 1 (default 50–100 items) will silently undercount metrics for large projects.
- JQL and GraphQL filter syntax differs subtly between tools — a prompt that works for Jira will fail verbatim on Linear; tool-specific prompt templates are mandatory.
- Slack Block Kit messages have a 3001-character limit per block; agents generating long tables must chunk or truncate with a "see full report" link.
- Scheduled agents that run at sprint boundaries may catch a "transitional" state where the old sprint is closed but the new one has no data yet — add a guard check before generating a report.
- Agents must not infer project health from a single metric; a sprint with 90% completion but 10 new scope-added issues is not actually healthy — multi-metric thresholds prevent false positives.
- Human checkpoint before sending executive-level reports — automated numbers can be technically correct but contextually misleading without narrative.

## References
- https://support.atlassian.com/jira-software-cloud/docs/create-and-customize-a-dashboard/ — Jira Dashboards
- https://linear.app/docs/insights — Linear Insights
- https://api.slack.com/block-kit — Slack Block Kit for structured messages
- https://docs.metabase.com/latest/api-documentation — Metabase REST API
- https://grafana.com/docs/grafana/latest/http_api/ — Grafana HTTP API
