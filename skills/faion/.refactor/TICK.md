# Refactor Pool — Tick & Orchestration Rules

**Project:** faion-network methodology refactor (5-file → new shape)
**Repo:** `/home/nero/workspace/projects/faion-net/faion-network`
**State home:** `skills/faion/.refactor/`
**Pool size:** 10 sonnet
**Batch size:** 8 paths
**Tick interval:** `/loop 5m`

## Hard rule for the parent (orchestrator) thread

The parent does NOT do refactor work. Parent ONLY:

- pop paths off `QUEUE.txt`
- dispatch background `Agent` subagents (model=sonnet, isolation=worktree, run_in_background=true)
- record outcomes to `DONE.txt`
- pull main / push main
- delete the `/loop` cron when queue empty
- restore failed batches to head of `QUEUE.txt` on quota exhaustion

If the parent starts editing methodology files itself, the abstraction is broken — stop and re-delegate.

## State files

| File | Tracked? | Purpose |
|------|----------|---------|
| `BRIEF.md` | yes | Subagent instructions (refactor procedure, quality gates, merge policy) |
| `TICK.md` | yes | This file — orchestration rules |
| `QUEUE.txt` | gitignored | Pending absolute paths, one per line |
| `DONE.txt` | gitignored | Tab-separated: `<path>\t<OK\|FAIL>\t<iso-date>\t[reason]` |

`QUEUE.txt` was built by `find` over `skills/faion/knowledge/` filtering for the OLD 5-file marker (has all of `README.md` + `checklist.md` + `templates.md` + `examples.md` + `llm-prompts.md`) AND excluding `geek/ai/ai-agents/*` (15 out-of-scope per migration note). Initial size: 1245 paths.

## Each tick (every 5 minutes via `/loop 5m`)

1. `cd /home/nero/workspace/projects/faion-net/faion-network`
2. `git pull --ff-only origin main` (pick up sibling-worktree merges)
3. Count active background agents from the most recent `<system-reminder>` listing OR via `TaskList`. Call this `active`.
4. Compute `slots = max(0, 10 - active)`.
5. If `slots > 0` AND `QUEUE.txt` is non-empty:
   - For each slot:
     - `head -8 QUEUE.txt` → `BATCH`
     - `sed -i '1,8d' QUEUE.txt` (atomic pop)
     - Dispatch one Agent (see "Dispatch shape" below)
6. Report ONE line: `Tick: pool=<active+new> queue=<remaining> done=<DONE.txt line count>`

## Dispatch shape

```
Agent({
  subagent_type: "general-purpose",
  model: "sonnet",
  isolation: "worktree",
  run_in_background: true,
  description: "Refactor batch: <first-target-basename>",
  prompt: `Read /home/nero/workspace/projects/faion-net/faion-network/skills/faion/.refactor/BRIEF.md and follow it end-to-end for the batch below.

CRITICAL: write files via worktree-relative paths (skills/...), NEVER absolute /home/... — those leak into main.

Run the MANDATORY pre-flight reads BEFORE any file write:
1. docs/skill-authoring.md
2. skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/templates/tag-glossary.xml
3. skills/faion/knowledge/geek/ai/llm-integration/semantic-xml-content/AGENTS.md (canonical example)

TARGETS:
<abs-path-1>
<abs-path-2>
...
<abs-path-8>`
})
```

## Completion handler (fires per task-notification from a background subagent)

1. `cd /home/nero/workspace/projects/faion-net/faion-network`
2. `git pull --ff-only origin main` (the subagent's flock'd merge already pushed)
3. Parse the subagent's stdout for the `PATHS:` block
4. Append each line to `DONE.txt`:
   ```bash
   for line in <PATHS-block>; do
     case "$line" in
       *: OK)   echo -e "${path}\tOK\t$(date -Iseconds)" ;;
       *: FAIL*) echo -e "${path}\tFAIL\t$(date -Iseconds)\t${reason}" ;;
     esac
   done >> skills/faion/.refactor/DONE.txt
   ```
5. If `QUEUE.txt` non-empty: pop next batch and dispatch replacement (same as tick step 5)
6. Report ONE line: `Pool=<active>: <prev-id> done (<accepted>/<batch_size>), replacement <new-id> dispatched. Queue=<rem> done=<total>.`

## Stop conditions

- **Queue empty + no active agents** → final `git push origin main`, `CronDelete <id>` for the `/loop` cron, report `complete: <K> batches, <M> methodologies refactored, <F> failed`.
- **3+ "out of extra usage" / quota errors in a 30-minute window** → `CronDelete <id>`, restore those 8-path batches to head of `QUEUE.txt`, alert user with the resume-time hint from the error.
- **User says stop** → `CronDelete <id>`, leave queue + worktrees as-is. Resume by re-launching `/loop` later — disk state survives.

## Resume on session restart / `/compact`

Disk state is the source of truth:

- `QUEUE.txt` — what's left
- `DONE.txt` — what's complete (sorted, deduplicated)
- `git log --since='<last tick time>'` — recent merges from sibling worktrees

If parent context lost agent IDs, just count active via `TaskList` and dispatch to refill the pool.

## Reporting cadence

- Per dispatch / completion: ONE line.
- Per tick: ONE line.
- Per stop: ONE line.

No per-file recap, no narration. The user reads `DONE.txt` and `git log` for detail.

## Gotchas

| Gotcha | Symptom | Fix |
|--------|---------|-----|
| Absolute path leak | Subagent writes to `/home/.../skills/...` from inside the worktree → file lands in main, not the worktree. | Repeat the warning verbatim in EVERY dispatch prompt. |
| Concurrent merge collision | Two worktrees race on ff-only merge. | `flock /tmp/faion-network-merge.lock` around the merge in `BRIEF.md`. |
| CHANGELOG.md conflict | All batches edit `## [Unreleased]`. | Resolve "keep both" entries during rebase. |
| Pre-commit fail | Lint/format issues. | Subagent fixes, re-stages, re-commits. NEVER `--no-verify`. |
| Queue head wrong after compact | Possible duplicate dispatch. | After pull, run `comm -23 <(sort QUEUE.txt) <(cut -f1 DONE.txt | sort -u)` to spot dupes. |
| `cwd` drift | `head: cannot open QUEUE.txt`. | Always prefix bash with `cd <repo-root>` before reading state files. |
