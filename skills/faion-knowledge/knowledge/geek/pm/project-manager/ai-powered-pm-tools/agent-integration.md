# Agent Integration — AI-Powered PM Tools 2026

## When to use
- Evaluating which AI-powered PM platform (Jira+Rovo, Monday.com, ClickUp, Wrike) fits the team's needs
- Integrating Claude subagents with an existing PM tool via its API to automate issue creation, work breakdown, or status reporting
- Setting up automated risk prediction or bottleneck detection workflows using PM tool AI features
- Generating work breakdown structures from project briefs using PM tool AI (Jira's AI Work Breakdown, ClickUp Brain)
- Automating meeting notes → task creation pipelines (Jira's Rewatch integration, ClickUp AI Notetaker)

## When NOT to use
- When the team has fewer than 3 people and project overhead from a full PM platform exceeds the coordination benefit
- For pure engineering execution tracking where a simple Linear or GitHub Issues workflow is sufficient
- When PM tool AI features require vendor-specific models that conflict with organizational data governance policies
- For critical path management in construction or hardware projects — nPlan is specialized; generic AI PM tools do not understand physical dependencies

## Where it fails / limitations
- AI work breakdown suggestions from Jira Rovo and ClickUp Brain are based on existing project patterns — novel project types generate less relevant suggestions
- ML risk prediction models (Wrike, Forecast App) require 3-6 months of historical project data before predictions become reliable
- AI-generated task descriptions and subtasks require human review — PM tool AI does not understand codebase-specific constraints or team conventions
- "No-code app generation" features (Monday vibe) produce prototypes that need significant refinement before production use
- Vendor lock-in risk: Jira Rovo agents, Monday Agent Factory, and ClickUp Autopilot agents are not portable across platforms

## Agentic workflow
Claude subagents can interact with PM tools via their REST APIs: read project backlogs, generate work breakdown for epics, create subtasks, update status fields, and generate sprint reports. The most reliable pattern is agent-as-scribe: agent reads meeting transcripts or brief descriptions and creates structured issues via API. Jira's REST API and Linear's GraphQL API are the most agent-friendly for this pattern. Human approval is required before the agent creates issues in production project boards — a staging area (draft issues, sandbox project) is the recommended pattern.

### Recommended subagents
- general Bash/HTTP subagent — Jira REST API, Linear GraphQL API, ClickUp REST API calls
- `faion-sdd-execution` — quality gate before converting SDD tasks to PM tool issues
- `faion-knowledge` — load pm/project-manager methodology for WBS and reporting templates

### Prompt pattern
```xml
<task>Create a work breakdown structure for this project brief.</task>
<brief>{{project_brief}}</brief>
<team_size>{{n}}</team_size>
<output_format>
  JSON array of issues:
  [{ "title": "", "type": "epic|story|task|bug", "description": "",
     "acceptance_criteria": [], "dependencies": [], "labels": [] }]
</output_format>
<constraints>
  - Maximum 3 levels of nesting (epic → story → task)
  - Each task must have at least one acceptance criterion
  - Flag any dependencies between epics
</constraints>
```

```bash
# Create Jira issues from JSON work breakdown
# Requires: JIRA_URL, JIRA_TOKEN, JIRA_PROJECT_KEY env vars
create_jira_issues() {
  local issues_json="$1"
  echo "$issues_json" | jq -c '.[]' | while IFS= read -r issue; do
    title=$(echo "$issue" | jq -r '.title')
    desc=$(echo "$issue" | jq -r '.description')
    curl -s -X POST "$JIRA_URL/rest/api/3/issue" \
      -H "Authorization: Bearer $JIRA_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"fields\":{\"project\":{\"key\":\"$JIRA_PROJECT_KEY\"},\"summary\":\"$title\",\"description\":{\"type\":\"doc\",\"version\":1,\"content\":[{\"type\":\"paragraph\",\"content\":[{\"text\":\"$desc\",\"type\":\"text\"}]}]},\"issuetype\":{\"name\":\"Story\"}}}"
  done
}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | Jira issue management from terminal | `go install github.com/ankitpokhrel/jira-cli/...@latest` / https://github.com/ankitpokhrel/jira-cli |
| `linear-cli` | Linear issue management | `npm i -g @linear/linear` / https://github.com/linearapp/linear |
| `curl` + `jq` | Direct REST/GraphQL API calls to PM tools | system packages |
| `clickup-cli` | ClickUp task management (community tool) | https://github.com/ramiandry/clickup-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (Atlassian) | SaaS | Yes — REST API v3 | Full REST API; Rovo agents API not yet public; workaround: standard issue CRUD |
| Linear | SaaS | Yes — GraphQL API | Best-in-class API for agents; rich query + mutation support |
| ClickUp | SaaS | Yes — REST API v2 | REST API covers tasks, lists, spaces; AI features not API-accessible |
| Monday.com | SaaS | Yes — GraphQL API | Monday API v2 supports board, item, column CRUD |
| Wrike | SaaS | Yes — REST API v4 | Risk prediction outputs not API-accessible; task CRUD is |
| Asana | SaaS | Yes — REST API | Mature API; webhooks for event-driven agent triggers |
| Notion | SaaS | Yes — API | Database pages as tasks; good for lightweight PM setups |
| GitHub Issues + Projects | OSS/SaaS | Yes — REST + GraphQL | Best choice for engineering-only teams; native CI/CD integration |

## Templates & scripts
See `templates.md` for sprint report and WBS templates.

Sprint report generation from Jira:
```bash
#!/bin/bash
# Generate sprint summary from Jira board
BOARD_ID="${1:?Usage: $0 <board_id>}"
SPRINT=$(curl -s "$JIRA_URL/rest/agile/1.0/board/$BOARD_ID/sprint?state=active" \
  -H "Authorization: Bearer $JIRA_TOKEN" | jq '.values[0]')
SPRINT_ID=$(echo "$SPRINT" | jq -r '.id')
SPRINT_NAME=$(echo "$SPRINT" | jq -r '.name')

ISSUES=$(curl -s "$JIRA_URL/rest/agile/1.0/sprint/$SPRINT_ID/issue" \
  -H "Authorization: Bearer $JIRA_TOKEN" | \
  jq '.issues[] | {key: .key, summary: .fields.summary, status: .fields.status.name}')

echo "Sprint: $SPRINT_NAME"
echo "$ISSUES" | jq -r '"[\(.status)] \(.key): \(.summary)"'
```

## Best practices
- Use PM tool AI features for initial work breakdown and Claude agents for context-aware refinement based on codebase knowledge — combine both rather than choosing one
- Always create a sandbox or template project for agent-generated issues before committing to the production board
- Set up webhooks from the PM tool to trigger agents on specific events (issue created, status changed to "blocked") rather than polling
- Monitor for the "AI productivity paradox" (DORA 2025): individual throughput metrics may improve while organizational delivery metrics stay flat — track end-to-end flow time, not just issue velocity
- Document which PM tool AI features are used and how — AI-assisted decisions should be traceable per PMBOK 8 AI appendix guidance

## AI-agent gotchas
- PM tool APIs have rate limits that agents can hit when bulk-creating issues — implement exponential backoff and batch creation with delays
- Jira's description field uses Atlassian Document Format (ADF), not plain text or Markdown — agents must generate ADF JSON, not plain text, for rich descriptions
- Monday.com GraphQL mutations require column IDs, not column names — agents must first fetch the board schema before creating items
- ClickUp's AI features (Brain, Autopilot) are not accessible via API — agents can only read/write standard task fields, not invoke AI-generated summaries
- Linear's GraphQL schema changes occasionally — agents relying on specific field names may break after platform updates; use schema introspection before bulk operations

## References
- https://developer.atlassian.com/cloud/jira/platform/rest/v3/ — Jira REST API v3
- https://developers.linear.app/docs/graphql/working-with-the-graphql-api — Linear GraphQL API
- https://clickup.com/api — ClickUp REST API v2
- https://developer.monday.com/api-reference/ — Monday.com GraphQL API
- https://github.com/ankitpokhrel/jira-cli — jira-cli terminal tool
- https://dora.dev/research/2025/ — DORA 2025: AI productivity paradox research
