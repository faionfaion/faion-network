---
name: faion-poll-agents
description: "Self-replenishing background-agent pool: dispatch N parallel worktree subagents on a queue of batched tasks, replace on completion, persist state to disk, drive via cron tick + completion handler."
tier: free
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, AskUserQuestion
---

> **Entry point:** `/faion-poll-agents` — invoke directly, or compose from `/loop` + `/schedule` for the cron tick.

# Self-Replenishing Agent Pool

**Communication: user's language. Code, docs, subagent prompts: English (saves ~30% tokens).**

## Purpose

Process a long queue of independent task batches by keeping a constant pool of N background subagents busy. Parent agent does **only** orchestration; all research, writes, commits, and merges happen inside isolated worktree subagents. Pool stays full via two complementary signals:

1. **Cron tick** — periodic top-up if the pool drained while parent was idle.
2. **Completion handler** — fired automatically when a background agent finishes; pops next batch and dispatches replacement.

This is the pattern used to enrich 1142 methodologies with `agent-integration.md` files in `faion-network/skills/faion/knowledge/**/*` (~140 batches × 8 paths each).

## Hard rule

The parent thread does NOT do research / writes / commits / merges. Parent ONLY:

- pop paths off `QUEUE.txt`
- dispatch background `Agent` subagents
- record outcomes to `DONE.txt`
- pull / push the bare repo
- delete the cron when queue empty
- restore failed batches on quota exhaustion

If parent starts editing files itself, the abstraction is broken — stop and re-delegate.

## Required state on disk (gitignored)

```
.research/
├── BRIEF.md       # research/work skeleton handed to each subagent (committed)
├── TICK.md        # orchestration rules, this file's source of truth (committed)
├── QUEUE.txt      # pending absolute paths, one per line (gitignored)
└── DONE.txt       # tab-separated: <path>\tOK\t<iso-date> (gitignored)
```

**Why disk and not in-memory:** parent context survives `/compact`, but the queue must survive *full session restart* too — cron lives in `~/.claude/` settings, but conversation context doesn't. Disk is the single source of truth.

`BRIEF.md` is the ONE source of truth for what each subagent should do — its skeleton, file format, commit style, merge policy. Edit `BRIEF.md`, not the dispatch prompt.

## Configuration knobs

| Parameter | Default | Notes |
|-----------|---------|-------|
| `pool_size` | 9 (Sonnet) / 3 (Opus) | Parallel slot target. Match to model quota. |
| `batch_size` | 8 paths per agent | Bigger = fewer dispatch turns; smaller = faster recovery on failure. |
| `model` | `sonnet` for bulk, `opus` for quality-critical | Subagent can pick own model based on task — see "Model selection" below. |
| `tick_interval` | `5m` | Cron tick. Short enough to recover from drained pool; long enough to not burn tokens. |
| `merge_lock` | `flock /tmp/<project>-merge.lock` | Serialize ff-only merges from concurrent worktrees. |

## Model selection

**Default:** if user doesn't specify, the orchestrator picks based on task character.

| Task character | Default model |
|----------------|---------------|
| Research, doc enrichment, mechanical text generation, summaries, factual lookups | `sonnet` |
| Architecture decisions, complex code with cross-file reasoning, security-sensitive work, multi-step planning | `opus` |
| Simple refactors, formatting, predictable transforms, small targeted edits | `haiku` |

**Mixed pool is fine.** If 5 of the 9 active agents are running Opus from earlier and a new dispatch goes to Sonnet, that's expected — agents are isolated and don't share state.

**User override always wins.** If user says "use sonnet" or "use opus", apply that to subsequent dispatches.

**Quota-aware fallback.** If 3+ batches return "out of extra usage" / "quota" errors in a window, halt the cron, restore failed batches to head of `QUEUE.txt`, alert user with the resume-time hint from the error (e.g. "9:30am UTC"). Don't silently retry — that wastes the recovery quota.

## Pool lifecycle

### Setup (one-time)

1. Build `QUEUE.txt`: list of all task targets, one absolute path per line.
2. Write `BRIEF.md`: full instructions a subagent needs (read-files, work-skeleton, commit-style, merge-policy, hard rules).
3. Write `TICK.md`: orchestration rules — this file's content, project-specific.
4. `.gitignore` entries for `QUEUE.txt`, `DONE.txt`, `.claude/worktrees/`.
5. Commit `BRIEF.md` and `TICK.md` so subagents in fresh worktrees can read them.
6. Schedule cron tick via `/loop <interval> <tick-prompt>` — the tick-prompt is the verbatim instruction block parent re-enters every interval.

### Dispatch (per-batch)

1. `cd <repo-root>` — always reset cwd; subagent worktrees can drift parent cwd on completion.
2. `git pull --ff-only origin main`.
3. `head -<batch_size> QUEUE.txt` to read next batch.
4. `sed -i '1,<batch_size>d' QUEUE.txt` to pop atomically.
5. Dispatch:

```
Agent({
  subagent_type: "general-purpose",
  model: "sonnet",                 // or opus / haiku per task character
  isolation: "worktree",           // creates fresh git worktree off main
  run_in_background: true,         // parent gets task-notification on finish
  description: "Batch: <short-label>",
  prompt: "Read <repo>/.research/BRIEF.md and follow it end-to-end for the batch below.\n\nCRITICAL: write files via worktree-relative paths (skills/...), never absolute /home/... — those leak into main.\n\nTARGETS:\n<absolute-path-1>\n<absolute-path-2>\n..."
})
```

6. Brief one-line update to user: `Pool=N: <prev-id> done, replacement <new-id> dispatched. Queue=M done=K.`

### Completion handler (fires per task-notification)

1. `cd <repo-root>`.
2. `git pull --ff-only origin main`.
3. Record done — extract paths from the latest commit's filenames:
   ```bash
   git log -1 --name-only --pretty=format: | grep agent-integration | sed 's|/agent-integration.md||' \
     | while read p; do echo -e "$repo/$p\tOK\t$(date -Iseconds)"; done >> DONE.txt
   ```
4. Pop next batch (`head -<batch_size>` then `sed -i '1,<batch_size>d'`).
5. Dispatch replacement.
6. One-line user update.

### Tick handler (fires per cron interval)

1. `cd <repo-root>` then `git pull --ff-only origin main`.
2. Count active background agents (`<system-reminder>` lines listing them, or just remember dispatch IDs).
3. If `active < pool_size` AND queue non-empty → for each missing slot pop `batch_size` lines and dispatch replacement (same as dispatch step).
4. `git push origin main`.
5. Report: `Tick: pool=N queue=M done=K`.

### Stop conditions

- **Queue empty + no active agents** → `git push`, `CronDelete <id>`, report `complete: K batches, M targets`.
- **3+ "out of extra usage" failures** → `CronDelete <id>`, restore those `batch_size`-path batches to head of `QUEUE.txt`, alert user with quota info.
- **User says stop** → `CronDelete <id>`, leave queue and worktrees as-is.

## Reporting cadence

**Per dispatch / completion:** ONE line.
> `Pool=9: <prev-id> done, replacement <new-id> dispatched. Queue=222 done=813.`

**Per tick:** ONE line.
> `Tick: pool=9 queue=222 done=813.`

**Per stop:** ONE line.
> `Done: 142 batches × 8 paths = 1136 enriched. 6 skipped.`

No per-file recap, no narration. The user reads diff and metrics, not chatter.

## Common gotchas

| Gotcha | Symptom | Fix |
|--------|---------|-----|
| **cwd drift** | `head: cannot open QUEUE.txt` after a subagent completion. | Always prefix bash with `cd <repo>` before relative paths, or use `$(pwd)/...`. |
| **Absolute-path leak** | Subagent writes to `/home/.../skills/...` → file lands in main repo's working tree, not the worktree. | Repeat warning verbatim in EVERY dispatch prompt: "CRITICAL: write via worktree-relative paths, never absolute". |
| **Concurrent merge collision** | Two ff-only merges race, one fails. | `flock /tmp/<project>-merge.lock` around `cd main; git fetch; git merge --ff-only` in BRIEF.md. |
| **CHANGELOG conflict** | Pre-commit hook requires CHANGELOG entry; concurrent batches edit same `## [Unreleased]` section. | BRIEF.md instructs agent to add ONE batch entry; conflicts resolve "keep both" — then re-merge. |
| **Pre-commit fail** | Merge blocked by lint/format. | Subagent fixes, re-stages, re-commits. NEVER `--no-verify`. |
| **Cron drift** | After `/compact` or session restart, parent forgets agent IDs. | Tick reads `git log` and `QUEUE.txt`/`DONE.txt`, not in-memory state. |
| **Queue head wrong** | Agent dispatched on already-done paths. | Run `comm -23 <(sort QUEUE.txt) <(cut -f1 DONE.txt | sort)` after merges to detect, prune duplicates. |

## Subagent type selection

| Subagent type | When to use |
|---------------|-------------|
| `general-purpose` | Default for research, code-writing, multi-tool batches. |
| `Explore` | Pure read-only investigation, no writes. Smaller context cost. |
| `Plan` | Architecture decisions, design before implementation. |
| Project-specific (e.g. `faion-sdd-executor-agent`) | Domain workflows with bespoke conventions. |

For pool work, `general-purpose` is almost always right because the BRIEF carries the conventions.

## Why this pattern works

- **Self-replenishing** — pool refills from two signals (tick + completion), so a stalled completion notification doesn't drain the pool indefinitely.
- **Disk state survives compaction** — parent can lose conversation context entirely and resume from `QUEUE.txt + DONE.txt + git log`.
- **Worktree isolation** — agents can't corrupt each other's branches; main only updated via locked ff-only merges.
- **Throughput dominated by parallel agents, not parent latency** — parent's job is small, mostly disk I/O and `git`.
- **Mixed-model pools work** — quota across Opus/Sonnet/Haiku is independent; you can run all three concurrently.

## Composition with other skills

- **`/loop <interval>`** drives the tick handler.
- **`/schedule`** for cron-style remote agents (when session might close).
- **`faion-brainstorm`** uses a *different* pool pattern (10 + 8 agents in two phases, no replenishment) — `faion-poll-agents` is for steady-state, brainstorm is for burst.
- **`faion`** is the canonical example: 1142 methodology directories, batch=8, pool=9, model=sonnet.

## Minimal example: tick prompt template

```
<project> research tick (batch mode, main-thread = orchestration only, pool=<N>, model=<M>).

Repo: <abs-repo-path>
Source of truth: <repo>/.research/TICK.md + BRIEF.md (committed).
State (gitignored): QUEUE.txt, DONE.txt.

HARD RULE: parent does NOT do research/writes/commits/merges. Only: pop paths → dispatch agents → record DONE → pull/push bare repo → delete cron when empty.

This tick:
1. cd repo. git pull --ff-only origin main.
2. Count active background agents.
3. If active < <N> AND QUEUE non-empty: for each missing slot pop <batch> lines (sed -i '1,<batch>d'), dispatch Agent(general-purpose, model: "<M>", isolation: "worktree", run_in_background: true) with prompt = "Read <repo>/.research/BRIEF.md and follow it end-to-end for the batch below.\n\nCRITICAL: write files via worktree-relative paths, never absolute — those leak into main.\n\nTARGETS:\n<batch absolute paths>".
4. git push.
5. Report: Tick: pool=N queue=M done=K.

On completion: pull, append <path>\tOK\t<iso-date> per target, pop next <batch>, dispatch replacement.

Stop: queue empty AND no active → push, CronDelete this job.

If 3+ batches return "out of extra usage" → CronDelete this job, alert user, restore those <batch>-path batches to head of QUEUE.

Never force-push, never --no-verify.
```

Drop into `/loop 5m <prompt>` and let it run.
