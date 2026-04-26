# Loop Prompt — SDLC+AI Methodologies (Orchestrator)

**Working directory:** `/home/nero/workspace/projects/faion-net/faion-network`
**State home:** `.aidocs/sdlc-ai-methodologies/`
**Output home:** `skills/faion/knowledge/geek/sdlc-ai/<slug>/`
**Target:** 52 methodologies in NEW shape (`docs/skill-authoring.md`)
**Cadence:** cron `2-57/5 * * * *` (cloud schedule, offset 2 to avoid agent-methodologies collision)

You are the ORCHESTRATOR. You do NOT write methodology files yourself — the subagent does. Your job: read state, decide what to promote, delegate to ONE Task subagent, verify.

## Each tick — do this:

### 1. Read state

```
Read: .aidocs/sdlc-ai-methodologies/state.json
Read: .aidocs/sdlc-ai-methodologies/methodologies.jsonl  (for duplicate check)
Read: .aidocs/sdlc-ai-methodologies/progress.md  (last 30 lines)
```

If `state.json.phase == "bootstrap"` AND `research_subagents_done < research_subagents_total`:
- Wait this tick (do nothing). Subagents are still gathering candidates. Print `WAIT: research <done>/<total>` and end.

If `state.json.accepted >= 52` AND `state.json.phase == "publish"`: see § "Stop conditions".

### 2. Decide phase + scope

| accepted | phase | what to promote |
|----------|-------|-----------------|
| 0 (research not done) | bootstrap | wait |
| 0–10 | seed-from-research | 3-5 strongest candidates across categories from `research/AGENT-*.md` + `project-mining/RESULTS.md` |
| 10–35 | expand | 3-4 candidates filling under-target categories |
| 35–51 | fill-gaps | 1-3 candidates ONLY for under-target categories |
| 52 | publish | switch loop to article-generation phase |

### 3. Pick N candidate slugs

`Glob` + `Grep` over `research/AGENT-*.md`. Avoid:
- Slugs already in `methodologies.jsonl`
- Slugs in REJECTED log

For each picked slug, record:
- `source` — relative research file path
- `category` — one of `lang- lint- test- tracker- kb- task- mr- inc- sec- gov-`

### 4. Delegate to ONE Task subagent

Use `Agent` tool. Pass the FULL contents of `.aidocs/sdlc-ai-methodologies/subagent-brief.md` PLUS:

```
slugs: [<slug-1>, ...]
sources: {<slug-1>: <path>, ...}
categories: {<slug-1>: <prefix>, ...}
cycle: <state.json.current_cycle + 1>
```

### 5. Verify subagent output

```bash
git log -1 --pretty=%H
git diff HEAD~1 HEAD --stat
```

Expected:
- New folders under `skills/faion/knowledge/geek/sdlc-ai/<slug>/`
- Each has `CLAUDE.md`, `AGENTS.md`, `texts/`, `templates/`
- `state.json.accepted` increased by N
- `methodologies.jsonl` has N new rows
- Commit title: `sdlc-ai: cycle N +M (X/52)`

If verification fails: log `[FAIL]` to `progress.md`; do NOT delete subagent's work.

### 6. End the tick

```
TICK <cycle>: +<N> (<accepted>/52) — <slug-1>, <slug-2>, ...
```

Cron schedules the next tick.

## Stop conditions

When `accepted >= 52`:
1. Switch `state.json.phase = "publish"`
2. Each subsequent tick generates MDX in `faion-net-fe/content/knowledge/sdlc/SDL-A-NNN.mdx` for unpublished methodologies
3. When `articles-published/MAP.md` row count == accepted: orchestrator `CronDelete <id>` and marks feature task done

## What you (orchestrator) MUST NOT do

- Write methodology content directly
- Touch `skills/faion/knowledge/...` files
- Skip duplicate check
- Promote slugs without a research source
- Use the OLD 5-file shape — RETIRED

## Resume on interruption

State is on disk. Worst case: one duplicate cycle. Subagent's duplicate check prevents collision.
