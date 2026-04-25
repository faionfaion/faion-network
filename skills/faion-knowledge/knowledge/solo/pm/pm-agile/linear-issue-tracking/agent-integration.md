# Agent Integration — Linear Issue Tracking

## When to use
- Automating sprint/cycle hygiene: moving stale issues, closing duplicates, adding labels
- Generating weekly velocity or cycle summary reports from issue data
- Syncing Linear issue state with GitHub PR status in CI pipelines
- Creating issues in bulk from structured input (SDD task lists, CSV backlogs)
- Drafting issue content (acceptance criteria, technical notes) from a spec or design doc

## When NOT to use
- Teams not using Linear — do not retrofit this workflow onto Jira, Trello, or GitHub Projects
- One-time exploratory tasks where creating an issue adds overhead, not value
- Real-time incident response — Linear's async model is too slow for live war-rooms
- Replacing human judgment on priority or roadmap sequencing

## Where it fails / limitations
- Linear's GraphQL API rate-limits at 1,500 req/10 min — batch operations on large workspaces hit ceiling fast
- Cycle scope decisions require human judgment; agents that auto-add issues to active cycles cause scope creep
- Label taxonomy drift: agents that create new labels without governance fragment the system over time
- Webhook delivery is not guaranteed — agent pipelines relying on webhooks need idempotent replay logic
- Linear does not expose time-series velocity data directly; agents must reconstruct it from issue history

## Agentic workflow
A Claude subagent reads a structured SDD task list or implementation-plan.md, maps each task to a Linear issue template, and creates issues via the GraphQL API with correct priority, label, and cycle assignment. A second pass agent can poll open issues nightly, detect blockers (issues in "In Progress" for >3 days with no comment), and post a Slack or Telegram digest. GitHub Actions integration lets a CI agent auto-transition issue status when a PR is opened or merged.

### Recommended subagents
- `faion-sdd-executor-agent` — converts SDD task blocks into Linear issue drafts and validates acceptance criteria completeness
- A generic GraphQL agent — executes mutations against the Linear API given structured issue payloads

### Prompt pattern
```
You are a PM automation agent. Given the implementation-plan.md below, create Linear issues for each TASK_ block.
For each task: title = task slug, description = task body, priority = complexity map (Low→No Priority, Medium→Medium, High→High, Critical→Urgent), label = task type (feat/fix/chore).
Return a JSON array of issue payloads ready for the Linear GraphQL createIssue mutation.
```

```
Given this Linear issue list (JSON), identify issues that have been "In Progress" for more than 3 cycle days with zero comments. Return a markdown digest with: issue ID, title, assignee, days stalled.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `linear-cli` (community) | Query and create issues from terminal | `npm i -g @linear/cli` / github.com/Taction/linear-cli |
| `gh` (GitHub CLI) | Link PR descriptions to Linear issue IDs | `brew install gh` / cli.github.com |
| `jq` | Parse Linear GraphQL JSON responses | `apt install jq` / stedolan.github.io/jq |
| `curl` | Raw GraphQL mutations against Linear API | built-in / developers.linear.app |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes — GraphQL API | Full CRUD on issues, cycles, projects, labels; webhook support |
| Linear Webhook | SaaS | Yes — event stream | Push events on issue state changes; requires HTTPS endpoint |
| GitHub Actions | SaaS | Yes | Official Linear GitHub integration auto-syncs PR → issue status |
| Zapier / Make | SaaS | Partial | No-code bridges; limited to pre-built triggers, not custom queries |
| n8n | OSS/SaaS | Yes | HTTP node can call Linear GraphQL; good for nightly digest automation |

## Templates & scripts
```bash
#!/bin/bash
# Create a Linear issue via GraphQL
# Usage: LINEAR_KEY=<key> TEAM_ID=<id> bash create_issue.sh "Title" "Description" "High"

TITLE="$1"
DESC="$2"
PRIORITY="$3"  # Urgent=1 High=2 Medium=3 Low=4 NoPriority=0

PRIORITY_MAP() {
  case "$1" in Urgent) echo 1;; High) echo 2;; Medium) echo 3;; Low) echo 4;; *) echo 0;; esac
}

P=$(PRIORITY_MAP "$PRIORITY")

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation { issueCreate(input: { teamId: \\\"$TEAM_ID\\\", title: \\\"$TITLE\\\", description: \\\"$DESC\\\", priority: $P }) { success issue { id identifier url } } }\"}" \
  | jq '.data.issueCreate.issue | {id, identifier, url}'
```

## Best practices
- Always set `teamId` explicitly — workspace-level mutations silently pick wrong team on multi-team orgs
- Use Linear's `attachmentCreate` mutation to link external docs (Figma, Notion) instead of pasting raw URLs in description
- Prefer `labelIds` over creating labels in automation; maintain a label registry document to avoid drift
- Cycle assignment via API should only target `nextCycle` or `futureCycle`, never the active cycle, to protect scope
- Store the Linear issue identifier (e.g., `BAK-123`) in git branch names and PR titles to enable bidirectional traceability
- Use `issueSearch` with filters rather than `issues` with client-side filtering — server-side filtering is 10x faster on large workspaces

## AI-agent gotchas
- Linear's `issueCreate` mutation does not validate that acceptance criteria are non-empty — agent must enforce this before calling the API
- GraphQL cursor-based pagination (`after` argument) must be implemented; agents that fetch only the first page silently miss issues
- Cycle IDs rotate every cycle; hardcoding a cycle ID in an agent breaks after 2 weeks — always resolve by querying `team.activeCycle` first
- Priority field is an integer enum (0–4), not a string; agents receiving natural-language priority must map explicitly
- Human-in-the-loop required before bulk-closing or bulk-reassigning issues — irreversible at scale and Linear has no batch undo
- Webhook secret verification is not optional; an agent endpoint without HMAC validation is an injection vector

## References
- https://developers.linear.app/docs/graphql/working-with-the-graphql-api
- https://linear.app/method
- https://linear.app/docs/keyboard-shortcuts
- https://developers.linear.app/docs/webhooks
- https://linear.app/integrations/github
