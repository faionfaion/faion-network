# Loop Prompt — Agent Methodologies (Orchestrator)

**Working directory:** `/home/nero/workspace/projects/faion-net/faion-network`
**State home:** `.aidocs/agent-methodologies/`
**Output home:** `skills/faion/knowledge/geek/ai/ai-agents/<slug>/`
**Target:** 50 methodologies in NEW shape (`docs/skill-authoring.md`)
**Cadence:** cron `*/5 * * * *` (cloud schedule)

You are the ORCHESTRATOR. You do NOT write methodology files yourself — that is the subagent's job. Your job is to read state, decide what to promote, delegate to ONE Task subagent, verify the result.

## Each tick — do this:

### 1. Read state

```
Read: .aidocs/agent-methodologies/state.json
Read: .aidocs/agent-methodologies/methodologies.jsonl  (for duplicate check)
Read: .aidocs/agent-methodologies/progress.md  (last 30 lines)
```

If `state.json.accepted >= 50` AND `state.json.phase == "publish"`: see § "Stop conditions" below.

### 2. Decide phase + scope

| accepted | phase | what to promote |
|----------|-------|-----------------|
| 0–14 | seed-from-research | 3-5 strongest candidates across categories from `research/AGENT-*.md` |
| 15–35 | expand | 3-4 candidates filling under-target categories (read `state.json.categories`) |
| 36–49 | fill-gaps | 1-3 candidates ONLY for categories where `accepted < target` |
| 50 | publish | switch loop to article-generation phase (separate brief) |

NOTE: There are 15 already-shipped methodologies in the OLD 5-file format. They count toward `accepted` but are NOT migrated. Every new methodology you promote MUST use the NEW shape from `docs/skill-authoring.md`.

### 3. Pick N candidate slugs

Use `Glob` + `Grep` to scan `research/AGENT-*.md` and any `candidates.md` entries. Avoid:
- Slugs already in `methodologies.jsonl`
- Slugs in `progress.md` REJECTED log

For each picked slug, record:
- `source` — relative research file path
- `category` — prefix (`so-/mm-/tu-/pl-/lp-/mem-/cli-/eval-/cost-/mcp-`)

### 4. Delegate to ONE Task subagent

Use the `Agent` tool (subagent_type=`general-purpose` or specialized SDD executor if available). Pass it the FULL contents of `.aidocs/agent-methodologies/subagent-brief.md` PLUS this tick's variables:

```
slugs: [<slug-1>, <slug-2>, ...]
sources: {<slug-1>: <path>, ...}
categories: {<slug-1>: <prefix>, ...}
cycle: <state.json.current_cycle + 1>
```

Subagent reads research, writes folders, updates state, appends progress, commits. Returns count + commit SHA.

### 5. Verify subagent output

```bash
git log -1 --pretty=%H
git diff HEAD~1 HEAD --stat
```

Expected:
- New folders under `skills/faion/knowledge/geek/ai/ai-agents/<slug>/`
- Each new folder has `CLAUDE.md`, `AGENTS.md`, `texts/`, `templates/`
- `state.json.accepted` increased by N
- `methodologies.jsonl` has N new rows
- One commit with title `agents: cycle N +M (X/50)`

If verification fails: log to `progress.md` with `[FAIL]` prefix, do NOT delete subagent's work, let next tick re-attempt or escalate.

### 6. End the tick

You do NOT schedule the next tick — cron does that. Just print:

```
TICK <cycle>: +<N> (<accepted>/50) — <slug-1>, <slug-2>, ...
```

## Stop conditions

When `accepted >= 50`:
1. Switch `state.json.phase = "publish"`
2. The loop continues, but each tick now generates MDX articles in `faion-net-fe/content/knowledge/agents/AGT-A-NNN.mdx` for any methodology not yet in `articles-published/MAP.md`
3. When `articles-published/MAP.md` row count == accepted: orchestrator runs `CronDelete <id>` and marks feature task done

The article-generation tick is documented separately (see § "Publish phase" in design.md).

## What you (orchestrator) MUST NOT do

- Write methodology content directly
- Touch `skills/faion/knowledge/...` files
- Skip the duplicate check
- Promote slugs that lack a research source
- Use the OLD 5-file shape (`README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`) — RETIRED

## Resume on interruption

State is on disk (`state.json`, `methodologies.jsonl`, `progress.md`). If a tick was killed mid-write: next tick reads state and resumes. Worst case: one duplicate cycle if previous didn't commit. Subagent's duplicate check prevents content collision.
