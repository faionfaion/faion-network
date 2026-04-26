# Agent Integration — Backlog Management

## When to use
- Backlog has >100 items and a "next sprint" that nobody trusts.
- Pre-grooming session: agent pre-classifies new items and flags stale ones for archive.
- After SDD `spec.md`/`design.md` lands: auto-decompose into INVEST stories with acceptance criteria.
- Cross-project rollup: when the same person owns 5+ backlogs (Linear/Jira/GitHub Projects).
- Migration between trackers (Trello → Linear, GitHub Issues → Jira).

## When NOT to use
- Solo founder, <30 items: a Markdown file beats agent automation. Scale matters.
- Backlog is a wishlist, not a commitment system — fix process before adding agents.
- Compliance-bound product (medical, aviation) where every state change needs human signoff and audit trail.

## Where it fails / limitations
- LLM-rewritten user stories drift from original intent — original requestor wording is signal, agent paraphrasing destroys it. Keep original under `### Raw request`.
- Acceptance-criteria generation is plausible-but-shallow: agent writes "user can do X" 3 times in different words. Force "Given/When/Then" and reject AC <3 distinct preconditions.
- Stale detection on activity timestamp alone is wrong — items can be valid and dormant. Cross-check with linked customer requests and roadmap.
- Estimate generation by LLMs is fiction; T-shirt sizing needs team calibration on past delivery, not agent guess.
- "Merge similar items" is high-stakes — wrong merges destroy audit trail and lose distinct customer requests.

## Agentic workflow
Three-pass: (1) `triage` agent runs nightly on new items: classify (feature/bug/debt/research), enrich with template, draft AC, propose priority — outputs draft, never auto-applies. (2) `health-check` agent runs weekly, produces backlog health report (counts, age distribution, AC coverage %, stale candidates). (3) `groomer` agent assists synchronous grooming: takes top-20 items, asks clarifying questions, refines in-place under human approval. Production rule: agents draft, humans commit. Use Linear/Jira/GitHub APIs to apply changes through PRs/changesets, never direct mutation.

### Recommended subagents
- `backlog-triage` — sonnet, classifies + drafts story format from raw request.
- `backlog-health` — haiku, computes metrics from API export.
- `backlog-groomer` — opus during real grooming session (multi-turn dialogue).
- `task-creator-agent` (already in repo `faion-task-creator-agent`) — decomposes spec → tasks.

### Prompt pattern
```
Raw request: {customer/team text}
Existing similar items: {top-3 by embedding similarity}
Output (do NOT auto-create):
- merge_candidate: {id or null with reasoning}
- story: As a {user}, I want {action}, so that {benefit}
- acceptance_criteria: 3-5 Given/When/Then
- size_estimate: XS/S/M/L/XL with rationale
- priority_proposal: P1/P2/P3 with criteria-based reasoning
- raw_request_preserved: {original text verbatim}
```

```
Backlog export {linear-export.json}.
Compute: total, by_status, by_type, age_buckets (0-30, 30-90, 90-180, 180+),
ac_coverage_pct, stale_candidates (180+ days no activity AND no
roadmap link). Return health report against targets:
ready=10-20, stale<10%, ac_coverage>80%.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `linear-cli` (community) | Linear backlog ops | `npm i -g @linear/sdk` |
| `gh issue` / `gh project` | GitHub Issues + Projects v2 | https://cli.github.com |
| `jira-cli` (Atlassian) | Jira read/write | https://github.com/ankitpokhrel/jira-cli |
| `notion-cli` | Notion-as-tracker | https://github.com/jevakallio/notion-cli |
| `trello-cli` | Trello migration source | OSS, npm |
| `claude` Skill tool | Drive sub-agents | https://docs.anthropic.com/en/docs/claude-code |
| `jq` + `csvkit` | Health-metric computation | system |
| `embedding-cli` (sentence-transformers) | Duplicate detection | `pip install sentence-transformers` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Excellent | GraphQL API, OAuth + PAT, webhooks. Best agent fit. |
| Jira Cloud | SaaS | Yes | REST + Forge; complex permissions; agent must scope tightly. |
| GitHub Projects v2 | SaaS | Yes (GraphQL) | Free for open source; tightly couples to repo. |
| Notion | SaaS | Yes | Backlog-as-database; weaker for sprint mechanics. |
| ClickUp | SaaS | Yes | API stable; verbose payloads. |
| Shortcut | SaaS | Yes | Simple REST; smaller ecosystem. |
| Trello | SaaS | Yes | Card-based; common migration source. |
| Plane.so | OSS | Yes | Linear-clone, self-host; webhooks; agent-friendly. |
| Backlog.com | SaaS | Limited | Niche; older API. |
| Asana | SaaS | Yes | Heavy-weight; project-centric. |

## Templates & scripts
See `templates.md` for Backlog Health Check, Grooming Agenda, Item Template.

```bash
#!/usr/bin/env bash
# backlog-health.sh — Linear example, run weekly via cron
set -euo pipefail
WEEK=$(date +%Y-W%V)
OUT=~/backlog/$WEEK
mkdir -p "$OUT"

# Pull all issues for team
curl -s -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ issues(filter:{team:{key:{eq:\"ENG\"}}}){ nodes { id title state { name } updatedAt priority labels { nodes { name } } } } }"}' \
  https://api.linear.app/graphql > "$OUT/issues.json"

# Health report
claude -p "$(cat ~/prompts/backlog-health.txt)" \
  --input-file "$OUT/issues.json" > "$OUT/health.md"

# Stale candidates
jq -r --arg cutoff "$(date -d '-180 days' -Iseconds)" \
  '.data.issues.nodes[] | select(.updatedAt < $cutoff) |
   "\(.id) | \(.title) | \(.updatedAt)"' \
  "$OUT/issues.json" > "$OUT/stale.txt"
```

## Best practices
- **Agents draft, humans commit**: every AI-proposed change goes through human approval. Never grant write-scoped tokens to autonomous agents.
- **Preserve raw requests verbatim**: agent rewrites lose nuance; keep `### Raw request` section.
- **DEEP not deep**: top 10 items detailed, bottom 100 one-liner — resist the urge to AC-everything.
- **Ready definition is binary, not vibe**: scope clear, AC present, estimated, no blockers — agent enforces this gate before sprint planning.
- **Stale = no activity AND no link**: timestamp alone is noise; cross-check with roadmap/customer linkage.
- **Estimate calibration with team baseline**: agents need 20 past completed items as priors, otherwise they all-S everything.
- **One source of truth**: don't sync Linear ↔ Jira ↔ Notion bidirectionally — pick one canonical, others are read-only views.
- **Limit "P1": if everything is P1, nothing is**. Agent should refuse to propose P1 if >20% of backlog is already P1.

## AI-agent gotchas
- API rate limits — Linear 1500 req/h, Jira tighter. Agents that re-pull on every action will throttle.
- LLMs invent customer types that match the wording — "as a power user", "as an admin" — when the raw request says nothing about role. Force quoting the request.
- Estimates without team-historical priors are dart-throws. Always bootstrap from last 30 closed items.
- Auto-merge bug: agents merging "similar" items lose distinct user voices; require 0.9+ similarity AND human accept.
- **Human-in-loop checkpoint**: prioritization is product-strategy territory. Agents propose; humans (PM/founder) decide.
- LLMs add fake dependencies ("blocked by X" with no evidence). Require source ticket or remove the field.
- Agent-applied edits to live tickets in front of users is jarring; route through staging branch / PR-style changeset.
- Token-cost trap: weekly full backlog scan on 1k+ items is expensive. Embedding-cluster first, then LLM only on changed clusters.

## References
- Mike Cohn — "Agile Estimating and Planning" (DEEP, INVEST origin)
- Marty Cagan — "INSPIRED" (chapter on backlog as strategic tool)
- Linear product docs — https://linear.app/docs/api
- GitHub Projects v2 GraphQL — https://docs.github.com/en/issues/planning-and-tracking-with-projects
- Atlassian — Jira REST API v3 docs
- "Lean Inception" by Paulo Caroli (story-mapping precursor)
