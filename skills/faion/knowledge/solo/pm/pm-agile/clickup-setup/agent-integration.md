# Agent Integration — ClickUp Setup

## When to use
- Setting up a new cross-functional workspace where engineering, product, marketing, and ops all need to track work in one tool.
- When migrating from Trello or Asana and need a richer hierarchy (Space → Folder → List → Task → Subtask) without switching to Jira.
- When OKR/goal tracking alongside task management is required in a single tool (ClickUp Goals feature).
- When time tracking and billing against tasks is needed — ClickUp has built-in time tracking with estimates.
- When the team wants highly customizable views (Gantt, Workload, Table, Board, Calendar) without a BI tool subscription.

## When NOT to use
- Engineering teams that need native Git PR integration as a first-class feature — ClickUp's GitHub integration is shallower than Linear or GitHub Projects.
- Large enterprises (500+ users) — ClickUp's performance degrades at scale and admin overhead is high.
- When the team has no dedicated ClickUp admin — ClickApps, automations, and custom field proliferation require ongoing governance.
- Simple kanban-only workflows — Trello is faster to set up and maintain.
- When the team is already fully productive in Linear or Jira — migration cost rarely outweighs incremental gains.

## Where it fails / limitations
- ClickUp API v2 is REST-only; no GraphQL. Complex queries (e.g., aggregated metrics across multiple lists) require multiple requests and client-side computation.
- Automations have a monthly execution limit per plan; heavy-automation workspaces on Business plan can exhaust the limit mid-month.
- Custom fields created at List level are not visible at Space or Folder level — field placement in the hierarchy must be planned upfront.
- Webhooks are workspace-wide, not per-list — agents receive events for all tasks and must filter by list/space ID client-side.
- The Workload view requires time estimates on tasks to compute correctly — if estimates are missing, workload shows empty.
- ClickUp's bulk update API (update multiple tasks) is limited to 100 tasks per request and does not support all field types.

## Agentic workflow
A Claude subagent can drive ClickUp workspace setup: it creates spaces, folders, and lists via API; applies custom field definitions; and seeds initial tasks from a backlog CSV or JSON. For ongoing operations, the agent can listen to ClickUp webhooks for task status changes, compute sprint metrics (completed tasks vs. committed), and post a daily digest to Slack. Automation configuration (native ClickUp automations) must be done through the UI, but agents can prepare the automation specifications as structured prompts for a human to implement. Agents should never delete tasks — set them to "Won't Do" status instead.

### Recommended subagents
- `clickup-workspace-bootstrapper` — given a workspace config JSON (spaces, folders, lists, custom fields), creates the full hierarchy via ClickUp API and returns created IDs.
- `clickup-sprint-reporter` — queries tasks in the current sprint list filtered by status; computes completion %, blocked count, overdue count; posts to Slack.
- `clickup-intake-agent` — webhook listener: on task creation in the Backlog list, validates required custom fields, assigns based on round-robin, adds a checklist template.

### Prompt pattern
```
Using the ClickUp API v2, fetch all tasks from list <LIST_ID>
where status is not in ["complete", "won't do"].
Include: id, name, status, priority, due_date, assignees, custom_fields.
Return JSON array. Read-only — do not modify any tasks.
```

```
Given this ClickUp workspace config: <config_json>
Create the following hierarchy via ClickUp API:
1. Space: <space_name> with these statuses: <statuses>
2. Folders: <folder_list> inside the space
3. Lists: <list_map> inside each folder
4. Custom fields at space level: <fields>
Return created IDs for all objects. Stop and report error on any failed request.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` + `jq` | Direct ClickUp REST API calls; no official CLI exists | OS package manager |
| `clickup-python` (community) | Python wrapper for ClickUp API v2 | `pip install clickup-python` |
| `httpie` | Friendlier HTTP client for API testing during setup | `pip install httpie` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ClickUp API v2 | SaaS | Yes | Full CRUD on tasks, lists, spaces, custom fields. 100 req/min rate limit. |
| Toggl Track | SaaS | Yes | Time tracking integration; syncs time entries to ClickUp tasks via API. |
| Slack (ClickUp app) | SaaS | Partial | Notifications only; cannot create ClickUp tasks from Slack without a bot. |
| GitHub (ClickUp integration) | SaaS | Partial | Links PRs to tasks via branch naming; no automatic status sync. |
| n8n | OSS/SaaS | Yes | ClickUp node + HTTP node; webhook trigger for task events; self-hostable. |
| Zapier | SaaS | Partial | ClickUp triggers/actions; limited to simple field mappings. |
| Make (Integromat) | SaaS | Yes | Full HTTP module; best for complex ClickUp → Slack or Notion flows. |

## Templates & scripts
See `templates.md` for the task template, folder structure YAML, and sprint planning dashboard widget config.

Python script to bootstrap a space with lists and custom fields:
```python
import os, requests

BASE = "https://api.clickup.com/api/v2"
HEADERS = {"Authorization": os.environ["CLICKUP_TOKEN"], "Content-Type": "application/json"}
TEAM_ID = os.environ["CLICKUP_TEAM_ID"]

def create_space(name, statuses):
    r = requests.post(f"{BASE}/team/{TEAM_ID}/space",
        headers=HEADERS,
        json={"name": name, "multiple_assignees": True,
              "statuses": [{"status": s, "type": "open", "color": "#4169e1"} for s in statuses]})
    r.raise_for_status()
    return r.json()["id"]

def create_list(space_id, folder_id, name):
    url = f"{BASE}/folder/{folder_id}/list" if folder_id else f"{BASE}/space/{space_id}/list"
    r = requests.post(url, headers=HEADERS, json={"name": name})
    r.raise_for_status()
    return r.json()["id"]

space_id = create_space("Product Dev", ["backlog", "ready", "in progress", "review", "complete"])
print(f"Space created: {space_id}")
```

## Best practices
- Plan the hierarchy depth before creating any spaces — changing Space → Folder → List structure after tasks exist requires manual migration.
- Create custom fields at the highest applicable level (Space > Folder > List) so they inherit downward; creating fields at List level means they must be recreated in every new list.
- Use ClickUp's native Automation to handle mechanical flows (auto-assign on status change, notify on overdue) before building agent-driven automations — native automations are cheaper to maintain.
- Document all created custom field IDs in a config file or environment variable — field IDs are UUIDs, not human-readable names, and are required for API updates.
- Apply task templates via automation ("task created in list X → apply template Y") rather than agents — templates applied by automation are instant and do not consume API calls.
- Archive (set to "Won't Do") rather than delete tasks — deleted tasks cannot be recovered and break any rollup or reporting that referenced them.

## AI-agent gotchas
- ClickUp API v2 requires the personal API token in the `Authorization` header (not `Bearer` prefix) — agents must use `"Authorization": "<TOKEN>"`, not `"Authorization": "Bearer <TOKEN>"`.
- Custom field values in task responses are returned as an array under `custom_fields`; agents must match by `id` (UUID) not by `name` — field names can change, IDs do not.
- ClickUp webhooks send task events with a `task_id` but not the full task object — agents must do a follow-up `GET /task/{task_id}` to fetch details.
- Rate limit is 100 requests/minute per token; a workspace-bootstrap agent creating 50 lists + 20 custom fields + 200 initial tasks will hit the limit; add exponential backoff on 429.
- ClickUp's bulk task update endpoint does not support custom field updates — each task's custom fields must be updated individually via `POST /task/{task_id}/field/{field_id}`.
- Human checkpoint required before bulk status changes (e.g., marking 100 backlog tasks as "Won't Do") — ClickUp has no bulk undo.

## References
- https://clickup.com/api — ClickUp API v2 reference
- https://university.clickup.com/ — ClickUp University (setup best practices)
- https://clickup.com/blog/clickup-api/ — API use case examples
- https://docs.clickup.com/en/articles/856285-automations — Native automations
- https://clickup.com/templates — Official workspace templates
