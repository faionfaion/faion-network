# Agent Integration — Reporting Basics

## When to use
- Standing up a fresh PM dashboard for a new project or release.
- Replacing ad-hoc status emails with a recurring, audience-tailored dashboard.
- Establishing a metrics framework before introducing OKRs / NorthStar reporting.
- Auditing existing dashboards: which are read, which are stale, which to retire.

## When NOT to use
- The team has fewer than ~5 issues per week — manual updates are faster than dashboards.
- Highly research / discovery work where outputs are documents not tickets.
- Pre-revenue founder mode: a daily Slack message is cheaper.

## Where it fails / limitations
- Reports become "status theater": pretty, ignored, never drive decisions.
- Vanity metrics (velocity, MTTR-without-context) lead teams to optimize for the metric, not the outcome.
- Dashboards drift from reality once their data sources change schema.
- Executive dashboards over-aggregate; root-cause investigation still needs ticket-level access.
- Real-time refresh is rarely needed and quietly burns API quota.

## Agentic workflow
Use a Claude subagent to assemble the dashboard spec (which widgets, which audiences, which thresholds), then generate the queries / API calls / configuration as code. The agent maintains the spec doc; humans approve threshold changes. Run a weekly "dashboard hygiene" subagent that flags widgets that haven't been opened in N days.

### Recommended subagents
- `faion-pm-agent` — drafts dashboard specs per audience and KPI mapping.
- General-purpose Claude subagent — translates spec into Jira JQL, Linear filters, GitHub Projects views.
- `faion-sdd-executor-agent` — stages dashboard config changes through review.

### Prompt pattern
```
Given audience <executives|managers|team> and goal <X>, propose
5–7 widgets. For each, list: metric formula, data source, refresh
cadence, threshold for green/yellow/red, the decision it enables.
Reject any widget that has no decision attached.
```

```
Audit dashboards under <path>. For each widget output: last-opened
date, decisions made from it in last 90 days, recommendation
(KEEP / FIX / RETIRE) with one-line rationale.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | Run JQL, fetch sprint data | `brew install ankitpokhrel/jira-cli/jira-cli` |
| `gh` | GitHub Projects fields + issue export | `brew install gh` |
| `glab` | GitLab Boards data export | `brew install glab` |
| `linear-cli` | Linear cycles, issue exports | https://github.com/evangodon/lr |
| `metabase-cli` | Programmatic Metabase dashboards | `pip install metabase-api` |
| `grafanactl` | Grafana dashboards as code | https://grafana.com/docs/grafana/latest/cli/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Dashboards | SaaS | REST | Native; gadget vocabulary is dated |
| Linear Insights | SaaS | GraphQL | Built-in flow metrics |
| Metabase | OSS / SaaS | REST | Best for SQL-backed dashboards |
| Grafana | OSS | REST + JSON | Strong for time-series + DORA-style metrics |
| Looker Studio | SaaS | API | Free, ties to Sheets/BigQuery |
| Hex | SaaS | API | Notebook + dashboard hybrid |
| Cumul.io / Plotly | SaaS | API | Embedding into product UI |
| GitHub Insights | SaaS | GraphQL | Eng-flow visibility on top of Projects |

## Templates & scripts
See `templates.md` for team / management / executive dashboard specs and KPI formulas. Inline JQL → counts script:

```bash
#!/usr/bin/env bash
# jira-kpi.sh — emit JSON of KPIs for one sprint.
sprint="${1:?sprint id}"
auth="${JIRA_USER}:${JIRA_TOKEN}"
base="${JIRA_HOST}/rest/api/3/search"
jql_done="sprint=$sprint AND status=Done"
jql_committed="sprint=$sprint"
done=$(curl -s -u "$auth" "$base?jql=$jql_done&fields=customfield_10016" | jq '.issues | map(.fields.customfield_10016) | add')
committed=$(curl -s -u "$auth" "$base?jql=$jql_committed&fields=customfield_10016" | jq '.issues | map(.fields.customfield_10016) | add')
jq -n --argjson d "$done" --argjson c "$committed" \
  '{done:$d, committed:$c, commitment_pct: ($d/$c*100)}'
```

## Best practices
- Every widget must answer "which decision does this enable?" Strip widgets without an answer.
- Keep top-level dashboards to ≤7 metrics; deeper detail lives one click down.
- Tie green/yellow/red thresholds to the team's commitment, not industry averages.
- Always show trend arrows next to absolute numbers; absolute alone is meaningless.
- Mobile-test executive dashboards — they get read in elevators and Ubers.
- Version dashboard configs in git; treat schema changes like code reviews.

## AI-agent gotchas
- LLMs love to add charts. Constrain by max-widget count per audience.
- Agents will fabricate KPI formulas — require explicit data-source field names.
- Forecasting from velocity needs ≥6 sprints of data; agents will project from 1–2 if not constrained.
- Avoid agents auto-filing Jira/Linear changes from dashboard rules; one bad rule cascades broadly.
- Ensure the agent labels each metric as leading or lagging; it conflates them silently.

## References
- "Information Dashboard Design" — Stephen Few.
- DORA metrics — https://dora.dev/.
- Atlassian agile reporting docs.
- "Measuring Continuous Delivery" — Steve Smith.
- Kanban metrics — https://kanbanguides.org/.
