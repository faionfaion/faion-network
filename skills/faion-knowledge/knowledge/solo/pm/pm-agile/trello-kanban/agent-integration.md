# Agent Integration — Trello Kanban

## When to use
- Small teams (2–8 people) that need a visual board fast without database schemas or field configuration.
- Non-technical stakeholders (marketing, ops, content) who find Jira or Linear intimidating.
- Projects with a simple linear flow where cards move left-to-right through 5–7 defined stages.
- When Butler automation handles 90% of repetitive moves (auto-archive done cards, assign on move) without custom code.
- Prototyping a new workflow — Trello boards are the fastest way to visualize a process before committing to a heavier tool.

## When NOT to use
- Engineering teams needing native Git/PR integration as a first-class feature — Trello's GitHub Power-Up is shallow.
- Projects requiring sub-tasks, epics, or multi-level hierarchy — Trello cards are flat; checklists are a poor substitute for sub-issues.
- Teams needing velocity tracking, cycle time analytics, or burndown charts without installing third-party Power-Ups.
- Large backlogs (500+ cards) — board performance degrades and visual scanning becomes impractical.
- Organizations requiring SSO, audit logs, or enterprise compliance — available only on Enterprise plan.

## Where it fails / limitations
- Trello has no native sprint/cycle concept — sprint boards require manual list management or the Trello Agile Sprint Board template Power-Up.
- Butler automation language is English natural-language syntax; complex conditional logic is difficult to express and debug.
- The REST API does not expose custom field values in the default card response — requires an extra request to fetch custom field items.
- Webhooks are per-board and must be re-registered if the board is copied or recreated.
- No bulk move or bulk update via API in a single call — each card requires a separate PUT request.
- Power-Ups count toward a per-board limit on free/Standard plans (1 per board on free); advanced automation requires Business Class.

## Agentic workflow
A Claude subagent can automate intake and triage: it watches a Trello webhook for new cards created in a "Backlog" list, fetches card details, applies appropriate labels based on title keywords, sets a due date using team conventions, and moves the card to "Ready for Dev" if it has a description and at least one checklist item. For reporting, an agent can query all cards on a board filtered by label or list and generate a markdown status digest for Slack. The agent uses the Trello REST API exclusively and should never delete cards — only archive them via `PUT /1/cards/{id}?closed=true`.

### Recommended subagents
- `trello-intake-agent` — triggered by webhook on card creation; validates description completeness, adds labels, assigns based on round-robin, posts a comment with next steps.
- `trello-standup-agent` — queries cards in "In Progress" and "Blocked" lists, formats a daily standup digest, posts to Slack.
- `trello-archive-agent` — weekly job: moves all cards in "Done" list older than 7 days to a dedicated "Archive" board or archives them on the current board.

### Prompt pattern
```
Fetch all cards from Trello list <LIST_ID> using the REST API.
Include: name, desc, labels, due, members, custom fields.
Return JSON array. Do not modify any cards.
```

```
Given this Trello card JSON: <card_json>
Determine the correct label set based on these rules:
- Title contains "bug" or "fix" → add label "Bug"
- Title contains "feat" or "add" → add label "Feature"
- Description is empty → add label "Needs Discussion", post comment "Description required before dev can start."
Apply via PATCH /1/cards/{id}. Return a summary of changes made.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `trello-cli` (community) | List boards, lists, cards from terminal | `npm install -g trello-cli`; needs API key + token |
| `curl` + `jq` | Direct REST API calls; quickest for one-off queries | OS package manager |
| `httpie` | Friendlier HTTP client for Trello API testing | `pip install httpie` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Trello REST API | SaaS | Yes | Full CRUD on boards/lists/cards/checklists. Rate limit: 300 req/10s per token. |
| Butler (native) | SaaS | Partial | Rule-based automation via UI only; not scriptable. |
| Zapier | SaaS | Partial | Trello triggers/actions; no custom code in free tier. |
| Make (Integromat) | SaaS | Yes | Full HTTP module; chain Trello reads + writes with logic branches. |
| n8n | OSS/SaaS | Yes | Trello node + HTTP node; self-hostable; webhook trigger works well. |
| GitHub Power-Up | SaaS | Partial | Links PRs to cards; no bi-directional status sync without Butler rules. |

## Templates & scripts
See `templates.md` for card description templates (Feature, Bug, Sprint Planning) and Butler rule YAML.

Minimal Python: fetch all in-progress cards and post to Slack:
```python
import os, requests

KEY   = os.environ["TRELLO_API_KEY"]
TOKEN = os.environ["TRELLO_TOKEN"]
LIST_ID      = os.environ["TRELLO_INPROGRESS_LIST_ID"]
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]

cards = requests.get(
    f"https://api.trello.com/1/lists/{LIST_ID}/cards",
    params={"key": KEY, "token": TOKEN, "fields": "name,due,idMembers"},
).json()

lines = [f"- {c['name']} (due: {c.get('due', 'none')})" for c in cards]
msg = "*In Progress*\n" + "\n".join(lines) if lines else "*In Progress*\nNo cards."
requests.post(SLACK_WEBHOOK, json={"text": msg})
```

## Best practices
- Define list names as verb phrases ("In Development", "Awaiting Review") so their meaning is unambiguous when agents filter by list name.
- Store the Trello API key and user token in environment variables — never embed them in card descriptions or board names where they appear in webhook payloads.
- Use custom fields (Story Points, Sprint) instead of encoding metadata in card titles — agents can query custom fields directly via API without text parsing.
- Keep WIP limits explicit in list names ("In Progress [WIP:3]") so humans and agents can check limits without a separate config file.
- Register webhooks at the board level, not per-card — fewer webhook registrations and you catch all card events in one stream.
- Archive cards rather than deleting — archived cards are still queryable via `GET /1/boards/{id}/cards?filter=closed` for history.

## AI-agent gotchas
- Custom field values are NOT included in the default `GET /1/lists/{id}/cards` response — agents must request `customFieldItems=true` as a query param or fetch separately.
- Trello API returns member IDs, not names — agents must resolve IDs via `GET /1/members/{id}` to produce human-readable reports.
- Butler rules run asynchronously; an agent that creates a card and immediately queries it may see the pre-Butler state (e.g., no label yet applied).
- Webhook model: Trello sends the entire card object on every change, not a diff — agents must compare against cached state to know what changed.
- Rate limit (300 req/10s) looks generous but is per token; an agent looping over 500 cards with extra custom-field fetches can hit it quickly.
- Human checkpoint required before bulk label changes or bulk archiving — there is no bulk undo in Trello.

## References
- https://developer.atlassian.com/cloud/trello/rest/ — Trello REST API reference
- https://trello.com/butler — Butler automation docs
- https://trello.com/power-ups — Power-Up directory
- https://trello.com/templates — Official board templates
