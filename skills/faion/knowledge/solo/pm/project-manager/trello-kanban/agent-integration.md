# Agent Integration — Trello Kanban

## When to use
- Small team (1-5 people) needs a visual kanban board with minimal setup overhead
- Project does not require cross-repository code traceability (no GitHub/GitLab deep linking needed)
- Stakeholders are non-technical and need a simple board they can update themselves
- Rapid prototyping or pre-MVP phases where flexibility beats structure
- Budget constraints: Trello Free is viable for teams under ~10 boards

## When NOT to use
- Team already on GitHub — GitHub Projects has tighter code integration; use that instead
- Complex dependency tracking needed — Trello lacks native dependency visualization
- OKR/goal tracking required — Trello has no goals layer; use ClickUp or Linear
- More than 3 boards needed under Free plan (Power-Ups limited to 1 per board on Free)
- Reporting or velocity metrics required regularly — Trello reporting is manual or requires Power-Ups

## Where it fails / limitations
- WIP limits are enforced by naming convention only ("In Progress (WIP: 3)") — not automatically blocked; human or Butler rule required
- Butler automation (native automation) cannot read external data or call arbitrary APIs; complex workflows need Zapier or n8n
- Trello REST API requires board/list/card IDs for all writes — agents must fetch IDs before creating/moving cards
- No native sprint burndown or velocity charts without Power-Ups (premium)
- Free-text card descriptions have no schema; agents reading cards must parse unstructured markdown

## Agentic workflow
An agent interacts with Trello via the REST API: it reads the board to get list IDs, queries cards by label or list, creates cards with structured descriptions (using the card template from templates.md), and moves cards between lists when status changes. Butler automation handles rule-based transitions (e.g., move card to Done when all checklists complete) so agents only need to trigger state changes via the API. The agent reports board state as a structured summary for human review.

### Recommended subagents
- General task subagent (claude-haiku) — card creation, label assignment, checklist population from templates
- Status reporter (claude-sonnet-4-6) — board state summary, stale card detection, WIP limit violation report

### Prompt pattern
```
Trello API base: https://api.trello.com/1
Auth: key={TRELLO_KEY}&token={TRELLO_TOKEN}

1. GET /boards/{board_id}/lists — retrieve list IDs
2. GET /lists/{list_id}/cards — read current cards in "Backlog"
3. For each card matching label "P0": POST /cards with idList={in_progress_list_id}
   Include description from the feature card template.
Report which cards were moved and current WIP count in "In Progress".
```

```
GET /boards/{board_id}/cards?fields=name,idList,labels,due,dateLastActivity
Find all cards where dateLastActivity < today-7 days AND idList != done_list_id.
Output: card name | list | days stale | assigned members.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `trello-cli` (npm) | CLI for reading/writing Trello boards | `npm i -g trello-cli` / https://github.com/mheap/trello-cli |
| `curl` + `jq` | Trello REST API calls from shell | system / https://developer.atlassian.com/cloud/trello/rest/ |
| `n8n` | Automate Trello workflows beyond Butler capability | self-hosted / https://n8n.io |
| `zapier` | No-code automation connecting Trello to 5000+ apps | SaaS / https://zapier.com/apps/trello |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Trello REST API | SaaS | Yes — REST | Full CRUD on boards, lists, cards, checklists, labels |
| Butler (native) | SaaS | Partial — rule-based | Agents configure rules via board settings; cannot call Butler API directly |
| Planyway | SaaS Power-Up | No direct API | Calendar/timeline Power-Up; no agent API |
| Unito | SaaS | Partial | Syncs Trello with GitHub/Jira/Asana; useful for cross-tool workflows |
| n8n | OSS | Yes — Trello node built-in | Best for agent-triggered automation beyond Butler |

## Templates & scripts
Card templates (Feature, Bug, Sprint Planning) are in `templates.md`.

Inline — create a Trello card via API:
```bash
#!/usr/bin/env bash
# trello-create-card.sh
KEY="${TRELLO_KEY:?set TRELLO_KEY}"
TOKEN="${TRELLO_TOKEN:?set TRELLO_TOKEN}"
LIST_ID="${1:?Usage: $0 list_id card_name}"
NAME="${2:?Usage: $0 list_id card_name}"
DESC="${3:-}"
curl -s -X POST "https://api.trello.com/1/cards" \
  -H "Content-Type: application/json" \
  -d "{\"key\":\"$KEY\",\"token\":\"$TOKEN\",\"idList\":\"$LIST_ID\",\"name\":\"$NAME\",\"desc\":\"$DESC\"}" \
  | jq '{id: .id, name: .name, url: .shortUrl}'
```

## Best practices
- Store TRELLO_KEY and TRELLO_TOKEN in environment variables or 1Password; never hardcode in agent prompts
- Add board ID and list IDs to the project's `.aidocs/memory/` or constitution so agents don't fetch them each session
- Use Power-Up "Custom Fields" for story points and sprint — agents can read/write these via the REST API custom fields endpoint
- Enforce card description template via a Butler button ("New Feature") that pre-fills the template text
- Archive the Done list at end of each sprint rather than deleting cards — preserves history for velocity tracking
- Limit labels to 8-12 maximum; agents produce label bloat when writing cards without a fixed label set
- Use `Card Aging` Power-Up to visually detect stale cards — agents can replicate this via `dateLastActivity` API field

## AI-agent gotchas
- Trello API requires board/list/card IDs (not names) for all write operations — agents must do a read pass first to map names to IDs
- Card descriptions are free-text markdown; agents reading cards must infer structure, not parse a schema — enforce templates at card creation to get consistent structure
- Butler rules are UI-configured only; agents cannot create or modify Butler rules via API — document automation rules in constitution.md
- Rate limit: 100 requests per 10 seconds per token — batch operations must respect this; parallel agent calls can hit it
- Moving a card to "Done" via API does not trigger Butler card-archived automation — separate API call needed if archiving is required
- Free plan Power-Up limit (1 per board) is a hard constraint for agent-enhanced boards

## References
- https://developer.atlassian.com/cloud/trello/rest/ — Trello REST API reference
- https://trello.com/butler — Butler automation documentation
- https://trello.com/power-ups — Power-Up directory
- https://support.atlassian.com/trello/ — Trello official documentation
- https://trello.com/templates — Board templates
