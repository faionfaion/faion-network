# Agent Integration — Notion PM (Agile)

## When to use
- Small agile team (2–10 people) that wants sprint planning, backlog, and documentation in a single Notion workspace without a separate PM tool.
- When sprint retrospectives, meeting notes, and task tracking need to live next to each other with inline cross-references.
- When the team's workflow is still evolving — Notion databases are the fastest to restructure compared to Jira or Linear.
- Solopreneur or micro-team practicing lightweight Scrum where full-featured sprint tooling (velocity charts, burndown) is overkill.
- When stakeholders need read-only access to project status via a shareable Notion page without creating PM tool accounts.

## When NOT to use
- Teams with mature Scrum practices needing native burndown charts, velocity tracking, and sprint analytics — Notion requires custom rollups and formulas to approximate these, and they are fragile.
- High-velocity engineering teams running 2-week sprints with 10+ members — Notion database performance degrades with large datasets and many concurrent editors.
- When issues need tight Git/PR integration (auto-close on merge, branch naming) — Notion has no native code integration.
- Organizations needing SOC2/HIPAA compliant issue tracking with field-level audit logs — Notion page history is per-page, not field-level.

## Where it fails / limitations
- Notion has no native sprint velocity or burndown chart — they must be computed via rollup formulas that break if relations are misconfigured.
- The Notion API does not support bulk operations — updating 50 task statuses requires 50 individual PATCH requests.
- Automations (native Notion) are limited to property triggers (not time-based) and cannot run scheduled jobs — external schedulers (n8n, cron) are required for daily standup digests.
- Relation fields break silently if the related page is deleted rather than archived; agents that hard-delete sprint pages corrupt task-to-sprint relations.
- Formula language cannot perform aggregations across databases — cross-database rollups require a relation + rollup chain, which has a max depth of 1 level.
- Rate limit is 3 requests/second per integration token; sprint planning with 100 tasks needs batching and backoff.

## Agentic workflow
A Claude subagent can automate the Notion agile cycle: before each sprint, it reads the backlog database (sorted by priority), selects the top N items by estimate that fit team capacity, updates their Sprint relation field to point to the new Sprint page, and posts a sprint plan summary to Slack. During the sprint, a daily agent can query tasks filtered to the current sprint where Status = "Blocked" and post a blocker digest. At sprint end, the agent can compute completion metrics via rollup property reads and fill in the Sprint page's Metrics table. All writes must go through the Notion API — agents should never use the Notion UI automation layer as it is not scriptable.

### Recommended subagents
- `notion-sprint-planner` — reads backlog database, ranks by priority/estimate, assigns top items to the current Sprint page, posts plan to Slack for human approval before saving.
- `notion-standup-agent` — daily: queries tasks in current sprint where Status = "In Progress" or "Blocked"; posts structured standup digest to Slack with links to Notion pages.
- `notion-sprint-closer` — at sprint end: reads Sprint page rollups (completed, incomplete, total), fills in Metrics table, sets Sprint status to "Completed", moves incomplete tasks to next sprint.

### Prompt pattern
```
Query Notion database <TASKS_DB_ID> for tasks where:
- Sprint relation = <CURRENT_SPRINT_PAGE_ID>
- Status != Done AND Status != Cancelled
Include: page_id, task title, assignee, status, estimate, blocked_by relation.
Return JSON array. Read-only.
```

```
Given this backlog JSON: <backlog_items>
and team capacity: <capacity_points>
Select tasks for the sprint:
1. Sort by Priority (Urgent > High > Medium > Low)
2. Include tasks until total Estimate >= capacity * 0.85
3. Do not split a task — include fully or skip
Return selected task page_ids and total estimate.
Await human approval before updating Sprint field via API.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `notion-client` (Python) | Full Notion API access: query/create/update pages | `pip install notion-client`; https://developers.notion.com/ |
| `curl` + `jq` | Ad-hoc REST API calls for debugging | OS package manager |
| `n8n` (CLI or self-hosted) | Schedule notion queries + Slack delivery without code | https://docs.n8n.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion API | SaaS | Yes | REST; 3 req/sec; full CRUD on pages/databases/blocks. |
| n8n | OSS/SaaS | Yes | Notion node; schedule-triggered; self-hostable; good for NERO stack. |
| Make (Integromat) | SaaS | Yes | Full HTTP + Notion module; best for complex cross-tool flows. |
| Zapier | SaaS | Partial | Notion triggers/actions; free tier limited to 1 step Zaps. |
| Slack API | SaaS | Yes | Deliver Notion-derived standup digests; Block Kit for formatting. |
| Notion2Sheets | SaaS | Partial | One-way export Notion database → Google Sheets for external reporting. |

## Templates & scripts
See `templates.md` for the full Task Template, Sprint Template, and Bug Report Template in Notion format.

Python snippet to assign selected backlog tasks to a sprint:
```python
import os, time
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])
SPRINT_PAGE_ID = os.environ["CURRENT_SPRINT_PAGE_ID"]

def assign_to_sprint(task_page_ids: list[str]):
    for page_id in task_page_ids:
        notion.pages.update(
            page_id=page_id,
            properties={
                "Sprint": {
                    "relation": [{"id": SPRINT_PAGE_ID}]
                }
            }
        )
        time.sleep(0.35)  # stay under 3 req/sec limit

# Usage: call after human approval
# assign_to_sprint(["page-id-1", "page-id-2", ...])
```

## Best practices
- Use a single Tasks database with Sprint as a relation field — never create a new database per sprint, which fragments history and breaks velocity computation.
- Define the Sprint page as the source of truth for sprint dates; use rollup properties on the Tasks database to derive "Is Current Sprint" rather than filtering by a hardcoded sprint name.
- Keep each task as a separate database page, not a sub-bullet inside a sprint document — only pages are queryable via the Notion API.
- Archive sprint pages (set a Status property to "Completed") rather than deleting — deleted pages break any task relation that pointed to them.
- For capacity planning, add an "Estimate" number property to every task and enforce it via a formula that flags missing estimates — agents need this field to compute sprint fit.
- Paginate all database queries with `start_cursor` — Notion returns max 100 items per request regardless of `page_size` parameter.

## AI-agent gotchas
- Notion API returns relation property values as `[{id: "page-uuid"}]` — agents must follow up with `pages.retrieve` to get the page title (sprint name, assignee name) for human-readable output.
- After creating or updating a relation, the rollup that depends on it may take 1–2 seconds to recalculate — agents querying rollup values immediately after a write may see stale data.
- Sprint "current" filtering: Notion has no native "current sprint" concept; agents must compare sprint page date properties with today using a formula or a filter with `date.after` / `date.before`.
- The `status` property type (introduced 2022) behaves differently from `select` in API responses — always check the property type before reading `status.name` vs `select.name`.
- Native Notion automations run asynchronously and cannot be triggered by the API — do not rely on them firing within a specific time window in an agent pipeline.
- Human checkpoint required before bulk sprint assignment (adding 30 tasks to a sprint via API) — review the plan output before calling `assign_to_sprint`.

## References
- https://developers.notion.com/reference — Notion API reference
- https://www.notion.so/help/automations — Native automations
- https://github.com/ramnes/notion-sdk-py — Python Notion SDK
- https://www.notion.so/templates/sprint-board — Notion sprint board template
- https://developers.notion.com/docs/working-with-databases — Querying databases guide
