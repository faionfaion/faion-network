# Agent Integration — ClickUp Setup

## When to use
- Team needs OKR/goal tracking alongside tasks in a single tool
- Project requires multiple view types in one workspace (Gantt, workload, board, list, calendar)
- Capacity planning and time tracking are required
- Migrating from a fragmented stack (Trello + spreadsheet + Notion + calendar) into one unified platform
- Team size justifies the setup investment (5+ people, multiple ongoing projects)

## When NOT to use
- Solo developer on a single project — ClickUp hierarchy overhead exceeds benefit; use GitHub Projects or a flat SDD file structure
- Team is already productive on a simpler tool (Trello, Linear) — migration cost is high without clear gain
- Short-lived project (under 4 weeks) — ClickUp workspace setup takes 1-2 days to configure properly
- GitHub code integration is the primary requirement — GitHub Projects is tighter for code-centric workflows
- Team has no designated ClickUp admin — the tool requires ongoing configuration management

## Where it fails / limitations
- ClickUp API v2 is the current stable version; some UI features (Sprints ClickApp, Workload view) have limited or no API coverage
- Automation trigger/action combinations are constrained; complex conditional logic needs Zapier or n8n
- Hierarchy depth (Workspace → Space → Folder → List → Task → Subtask) is powerful but becomes a maintenance burden without a clear hierarchy convention
- Template application via API is not supported — agents must create tasks with the template content inline
- Custom field writes require the field_id, which must be fetched per List — agents need a preliminary read pass

## Agentic workflow
An agent interacts with ClickUp via REST API v2: it queries spaces and folders to get IDs, creates tasks in the correct list with pre-populated custom fields (story points, sprint, component), and updates task status as work progresses. Automation handles mechanical status transitions (assignee triggers, due date notifications). Agents focus on: batch task creation from impl-plan, status reporting, sprint planning (assigning tasks to sprint custom field), and overdue detection. The ClickUp API uses personal tokens; store them in environment variables.

### Recommended subagents
- General task subagent (claude-haiku) — task creation, status updates, custom field population
- Planning subagent (claude-sonnet-4-6) — sprint planning, workload summary, overdue escalation report

### Prompt pattern
```
ClickUp API base: https://api.clickup.com/api/v2
Auth header: Authorization: {CLICKUP_TOKEN}

1. GET /team/{team_id}/space — get space IDs
2. GET /space/{space_id}/folder — get folder IDs for "Feature Development"
3. GET /folder/{folder_id}/list — get list ID for "Current Sprint"
4. POST /list/{list_id}/task for each task in implementation-plan.md Wave 1:
   {name, description, status: "ready", priority: 2, custom_fields: [{id: story_points_field_id, value: 3}]}
Report: created task IDs and names.
```

```
GET /list/{list_id}/task?due_date_lt={today_ms}&status=in+progress
Output: task name | assignee | due date | days overdue.
For each overdue task: POST /task/{task_id}/comment with body "Task is overdue — please update status or due date."
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `clickup-cli` (community) | CLI for basic ClickUp task operations | `npm i -g clickup-cli` / https://github.com/icapps/clickup-cli |
| `curl` + `jq` | ClickUp REST API v2 calls from shell | system / https://clickup.com/api/clickupreference/operation/GetAuthorizedTeams/ |
| `n8n` | ClickUp automation beyond native automation | self-hosted / https://n8n.io (ClickUp node built-in) |
| `Toggl Track` | Time tracking integration for billable work | SaaS / https://toggl.com/track/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ClickUp REST API v2 | SaaS | Yes — REST | Full task/list/folder CRUD; custom fields require field_id lookup |
| ClickUp Webhooks | SaaS | Yes | Trigger external agents on task status change, comment, assignment |
| n8n ClickUp node | OSS | Yes | Best for agent-triggered automation beyond native ClickUp automations |
| Zapier | SaaS | Partial | 1000+ ClickUp triggers/actions; no agent-native interface |
| Unito | SaaS | Partial | Two-way sync ClickUp ↔ GitHub/Jira/Trello |
| Toggl | SaaS | Yes — REST API | Time tracking data → ClickUp task estimates comparison |

## Templates & scripts
Task template (description format) is in `templates.md`. Folder/List structure example for software projects is in the README.

Inline — bulk-create tasks in a ClickUp list from a newline-delimited task name file:
```bash
#!/usr/bin/env bash
# clickup-bulk-create.sh
TOKEN="${CLICKUP_TOKEN:?set CLICKUP_TOKEN}"
LIST_ID="${1:?Usage: $0 list_id tasks_file}"
TASKS_FILE="${2:?}"
while IFS= read -r task_name; do
  [ -z "$task_name" ] && continue
  response=$(curl -s -X POST "https://api.clickup.com/api/v2/list/$LIST_ID/task" \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$task_name\", \"status\": \"backlog\"}")
  task_id=$(echo "$response" | jq -r '.id')
  echo "Created: $task_name (ID: $task_id)"
done < "$TASKS_FILE"
```

## Best practices
- Map ClickUp hierarchy to your org before setup: Space = product/team, Folder = project/initiative, List = workflow stage; document in constitution.md
- Create custom fields at Space level, not List level — agents can then use the same field_id across all lists in the space
- Store team_id, space_ids, folder_ids, list_ids, and custom field_ids in `.aidocs/memory/` — ClickUp API requires IDs for all operations; re-fetching each session wastes tokens and API quota
- Enable Sprints ClickApp at Space level before sprint planning; it cannot be added retroactively to tasks created before activation
- Use webhooks to trigger external agents on task events rather than polling; set webhook at space level for broad coverage
- Limit automation rules to 20 per space (Free plan); document each automation in a "Automation Inventory" doc
- Test automations on a dummy task before enabling — circular triggers (A triggers B triggers A) are a common failure mode

## AI-agent gotchas
- ClickUp API uses millisecond timestamps for due dates (Unix ms, not ISO 8601) — agents must convert dates before API calls
- Custom field writes require the exact field_id UUID; agents hallucinate plausible-looking UUIDs if not grounded — always fetch field_ids in a preliminary read step
- Template application is not available via API — agents must inline template content in task descriptions; keep templates in a shared file agents can read
- Automation loops are possible when agents update status fields that trigger automations that update status — disable conflicting automations before agent runs
- ClickUp rate limit: 100 requests/minute per token on Free plan — batch task creation for large impl-plans must pace requests
- Subtask creation requires parent task ID; agents creating a task hierarchy must create parent tasks first (sequential, not parallel)

## References
- https://clickup.com/api — ClickUp API v2 reference
- https://docs.clickup.com/ — ClickUp official documentation
- https://university.clickup.com/ — ClickUp University (setup walkthroughs)
- https://clickup.com/templates — Workspace templates
- https://n8n.io/integrations/clickup/ — n8n ClickUp integration
