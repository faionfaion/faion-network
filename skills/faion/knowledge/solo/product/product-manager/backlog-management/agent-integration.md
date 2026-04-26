# Agent Integration — Backlog Management

## When to use
- Backlog has crossed ~80 items and signal is degrading; weekly grooming has lapsed.
- Multiple input streams (support, sales, eng, founder ideas) need triaging into a single ranked list.
- Refining the top of backlog into "Ready" items before sprint planning.
- Auditing backlog health (DEEP/INVEST compliance) before a quarterly review.

## When NOT to use
- Pre-PMF prototype phase with <20 items — use a simple Trello/Notion list, not a managed backlog.
- One-off project with a fixed scope and end date — use a WBS or kanban board.
- When the team will not run weekly grooming. An unmaintained "managed backlog" is just a longer dumping ground.
- Replacing prioritisation frameworks. Backlog management organises items; RICE/MoSCoW prioritises them. Run prioritisation first.

## Where it fails / limitations
- Stale items accumulating because nobody dares delete; LLMs replicate this by archiving conservatively.
- "Ready" definition diluted to "has a title", which makes sprint planning slow.
- Acceptance criteria pasted from feature requests, not authored — generic, untestable.
- Single backlog conflating product, tech debt, bugs, and research; agents need a type field to triage correctly.
- Backlog tools without API (offline spreadsheets) cap automation; agents become advisory only.

## Agentic workflow
A capture agent normalises new inputs (issues, support tickets, feedback) into the backlog item template. A grooming agent runs on a schedule: deduplicates, archives stale (>180 days no activity), flags items missing acceptance criteria. A refiner agent picks top-N items and proposes ready-state edits — splitting, adding AC, sizing. A health agent emits the backlog health-check table monthly. Humans approve archive lists and final priority order.

### Recommended subagents
- `faion-task-creator-agent` — referenced in `README.md`; primary author for new backlog items.
- `faion-spec-reviewer-agent` — checks acceptance criteria for testability.
- `faion-mlp-impl-planner-agent` — links high-priority items back to roadmap themes.
- `faion-mvp-scope-analyzer-agent` — second opinion when an item is too big and needs slicing.

### Prompt pattern
```
System: You are a backlog refiner. Output JSON only.
For each input item produce:
  {id, type: feature|bug|tech_debt|research,
   title, story:"As a … I want … so that …",
   acceptance:[{given, when, then}], size: xs|s|m|l|xl,
   priority: p1|p2|p3, ready: bool, blockers:[], rationale}
Reject items where ready=true but acceptance is empty or size is missing.
```

```
System: You are a backlog hygiene agent. Given backlog.json:
  - mark stale = (last_activity > 180d AND priority != p1),
  - propose merges by title similarity > 0.85,
  - propose deletes for items duplicated by issue links.
Output: {archive:[ids], merge:[[a,b]], delete:[ids], reasons:{id: text}}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh issue` / `gh project` | Mass-edit GitHub issues with JSON payloads | https://cli.github.com/manual |
| `linear-cli` | Bulk operations on Linear backlog | https://developers.linear.app |
| `jira-cli` | JQL-driven cleanup and refinement | https://github.com/ankitpokhrel/jira-cli |
| `gitlab-cli` (`glab`) | Same for GitLab | https://gitlab.com/gitlab-org/cli |
| `pivotaltrackerctl` (community) | Legacy Pivotal Tracker batch ops | https://pivotaltracker.com/help/api |
| `claude-code` `Skill(faion-task-creator-agent)` | In-loop refinement during planning | repo `agents/` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes (GraphQL) | Best DX for agent CRUD on backlog. |
| Jira | SaaS | Yes (REST) | Most extensive but verbose API. |
| GitHub Issues + Projects v2 | SaaS | Yes (GraphQL) | Free for solo, integrates with code. |
| Plane | OSS | Yes (REST) | Self-host alternative to Linear. |
| OpenProject | OSS | Yes (REST) | Heavy but enterprise-grade. |
| Productboard | SaaS | Yes (REST) | Better for inputs intake than internal backlog. |
| ClickUp | SaaS | Yes (REST) | Custom statuses helpful for "ready" gates. |
| Notion DB | SaaS | Yes (REST) | Cheap, weak validation. |

## Templates & scripts
See `README.md` for Backlog Health Check, Grooming Agenda, and Item templates. Inline DEEP scorer to gate "ready" promotions:

```python
import sys, yaml
b = yaml.safe_load(open(sys.argv[1]))
ready = [i for i in b["items"] if i.get("ready")]
errs = []
for i in ready:
    if not i.get("acceptance"): errs.append(f"{i['id']}: ready but no AC")
    if not i.get("size"): errs.append(f"{i['id']}: ready but no size")
    if i.get("blockers"): errs.append(f"{i['id']}: ready but has blockers")
    story = i.get("story", "")
    if "As a" not in story or "I want" not in story or "so that" not in story:
        errs.append(f"{i['id']}: story missing INVEST shape")
if len(ready) < 8 or len(ready) > 25:
    errs.append(f"ready bucket size {len(ready)} out of 8..25 healthy range")
stale = [i for i in b["items"] if i.get("days_since_activity",0) > 180]
if len(stale) / max(len(b["items"]),1) > 0.10:
    errs.append(f"stale ratio {len(stale)/len(b['items']):.0%} > 10%")
for e in errs: print("FAIL:", e)
sys.exit(1 if errs else 0)
```

## Best practices
- Tag every item with type (feature/bug/tech_debt/research). Mixed-type backlogs cannot be reasoned about.
- Maintain four buckets — Ready, Upcoming, Backlog, Icebox — and enforce promotion criteria; otherwise the bucket model is decoration.
- Archive aggressively (180-day rule). The cost of re-creating a forgotten idea is lower than the cost of confusion from stale items.
- Acceptance criteria as Given/When/Then. Anything else fails sprint planning.
- Cap top-of-backlog to ~2 sprints of capacity. Beyond that, refinement is wasted work.
- Run a monthly health check with the metrics in `README.md`. Trend matters more than absolute numbers.
- Pair with prioritisation method; a backlog without a documented prioritisation method drifts to whoever speaks loudest.
- Source-link every item to its origin (ticket URL, customer quote, dashboard chart). No source ⇒ archive candidate.

## AI-agent gotchas
- Models generate AC like "User should be able to use the feature successfully." Require ≥2 G/W/T statements with concrete subjects.
- Stories collapse to "As a user…" because no persona is given; inject persona context per refinement.
- Sizing from an LLM is inconsistent across runs; treat it as relative within one batch only, never as absolute estimates.
- Auto-merge by title similarity false-positives on plurals/synonyms; always require human approval before merging issues with linked PRs.
- Auto-archive is the most dangerous op; archive should be a separate "proposed" status, not direct deletion.
- Multi-tenant backlogs (multiple products) confuse agents; partition by product before refinement.
- Token cost: refining 50 items ≈ 30–40k tokens output; chunk in 10s.
- Drift between backlog tracker and refined doc — always write back to the source of truth, never keep a parallel JSON.
- INVEST principle is often violated with "Independent" — agents will introduce hidden dependencies. Add a `dependencies` field and validate in the linter.

## References
- Mike Cohn — *User Stories Applied* (INVEST origin).
- DEEP backlog principles — Roman Pichler: https://www.romanpichler.com/blog/make-your-product-backlog-deep/
- Atlassian — backlog grooming guide: https://www.atlassian.com/agile/scrum/backlogs
- Scrum Guide 2020: https://scrumguides.org/scrum-guide.html
- Marty Cagan — *Inspired*, sections on the discovery-delivery boundary.
- Linear — "How we manage our backlog": https://linear.app/blog
