# Agent Integration — Notion PM

## When to use
- Solopreneur or small team needing a single workspace that combines project tracking, documentation, and wiki without switching tools.
- Projects where tasks are tightly coupled to long-form specs, design docs, or meeting notes living in the same tool.
- When the schema is uncertain and will evolve — Notion databases are cheap to restructure compared to Jira or Linear.
- Automating intake flows where external sources (forms, webhooks) need to create structured pages in a database.
- When stakeholders want a human-readable project view without accessing a dev-specific tool.

## When NOT to use
- Engineering teams that need deep Git/PR integration as a first-class citizen — Linear or GitHub Projects are better.
- High-volume issue tracking (1000+ issues/month) — Notion databases degrade in performance at scale.
- Teams that need built-in time tracking, burndown charts, or sprint velocity without custom rollup hacks.
- Regulated environments requiring detailed audit logs per change — Notion's page history is per-page, not field-level.

## Where it fails / limitations
- Notion API is eventually consistent; rapid sequential writes from an agent can create race conditions in rollups.
- No native webhooks for outgoing events — must poll or use third-party (Zapier/Make) to detect changes.
- Relations and rollups break if the related page is deleted rather than archived; agents that hard-delete records corrupt rollup counts.
- Formula language (as of 2025) lacks recursion and complex aggregations; agents cannot compute cross-database aggregations via formula alone.
- Rate limits: 3 req/sec per integration token; bulk operations must be batched with backoff.
- Board views cannot be filtered by more than one "group by" field — cross-dimensional reporting requires a separate filtered view.

## Agentic workflow
A Claude subagent can act as a PM orchestrator: it reads the Tasks database (filtered to a sprint or assignee), identifies blocked or overdue items, drafts status updates as page comments, and posts a daily digest to Slack via a webhook. For intake, an agent can parse inbound emails or form submissions and call `notion.pages.create` to populate a structured task page with pre-filled properties. Agents should never delete Notion pages — archive them by setting a Status property to "Cancelled" to preserve rollup integrity.

### Recommended subagents
- `pm-status-reporter` — queries the Tasks database, identifies overdue and blocked items, composes a plain-text digest, posts to Slack.
- `notion-intake-agent` — parses structured input (CSV, JSON, form payload) and creates Notion pages in the correct database with all required properties pre-filled.
- `pm-sprint-planner` — reads backlog items from a Notion database, scores by priority/estimate, and moves selected items into the current Sprint relation.

### Prompt pattern
```
Given the following Notion database schema: <schema>
Query tasks where Status != Done and Due Date < today.
For each: output JSON with {page_id, task_name, assignee, days_overdue}.
Do not delete any pages.
```

```
Create a new Notion page in database <db_id> with these fields: <fields_json>.
Use the Notion API. If a required field is missing, set it to "Backlog" for Status or 0 for Estimate.
Return the page URL on success.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `notion-cli` (community) | Unofficial CLI for Notion API queries | `pip install notion-client` (Python SDK); docs: https://developers.notion.com/reference |
| `httpie` / `curl` | Ad-hoc API testing against Notion REST endpoints | OS package manager |
| `jq` | Parse Notion API JSON responses in shell pipelines | `apt install jq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion API | SaaS | Yes | REST + official SDKs (JS, Python). 3 req/sec limit. |
| Zapier | SaaS | Partial | Trigger on Notion page creation/update; no custom code in free tier. |
| Make (Integromat) | SaaS | Yes | Full HTTP module; can chain Notion reads + writes with logic branches. |
| n8n | OSS/SaaS | Yes | Self-hostable; Notion node supports create/update/query. Good for NERO stack. |
| Notion2Sheets | SaaS | Partial | One-way sync Notion → Google Sheets for reporting; no write-back. |

## Templates & scripts
See `templates.md` for full database YAML schemas and task/sprint page templates.

Minimal Python snippet to query overdue tasks:
```python
import os
from notion_client import Client
from datetime import date

notion = Client(auth=os.environ["NOTION_TOKEN"])
today = date.today().isoformat()

results = notion.databases.query(
    database_id=os.environ["TASKS_DB_ID"],
    filter={
        "and": [
            {"property": "Status", "status": {"does_not_equal": "Done"}},
            {"property": "Due Date", "date": {"before": today}},
        ]
    },
).get("results", [])

for page in results:
    title = page["properties"]["Task"]["title"][0]["plain_text"]
    due = page["properties"]["Due Date"]["date"]["start"]
    print(f"{title} — due {due}")
```

## Best practices
- Use a single canonical Tasks database with linked views on sprint/project pages instead of creating separate databases per sprint — rollups stay accurate and archiving is simpler.
- Store the `database_id` and `integration_token` in environment variables or a secrets manager; never hardcode in agent prompts.
- Always set a Status property to "Cancelled" instead of deleting pages; deletion silently breaks rollups pointing to the deleted page.
- When writing via API, include all required select/status properties to avoid Notion creating orphan "Unknown" option values in your schema.
- Use `archived: true` on the page update endpoint to soft-delete instead of the delete endpoint — it preserves page history and relations.
- Paginate query results with `start_cursor` — Notion returns max 100 items per request regardless of `page_size`.

## AI-agent gotchas
- Notion's eventual consistency means a page created in one API call may not appear in a database query for 1–2 seconds; add a short retry/poll loop after create-then-query patterns.
- The API returns relation property values as arrays of `{id}` objects, not human-readable names — agents must do a follow-up `pages.retrieve` call to resolve titles.
- Formula properties are read-only via API; agents cannot set them directly and must update the underlying source properties instead.
- Agents should not batch-update more than 3 pages/sec or they will hit rate limits silently (200 response but queued, leading to stale state).
- Human checkpoint required before bulk status changes (e.g., marking 50 tasks as Done from a script) — Notion has no native undo for bulk API writes.
- The `notion-client` Python SDK does not raise exceptions on 429 rate limit responses by default; wrap calls with explicit status code checks.

## References
- https://developers.notion.com/reference — Official API reference
- https://www.notion.so/help/automations — Native automations docs
- https://github.com/ramnes/notion-sdk-py — Python SDK
- https://www.notioneverything.com/notion-api-limits — Community-documented rate limits
