# Research Tick — Batch Mode (5-10 methodologies per agent)

**Policy:** keep 5 subagents concurrently active. Each agent processes a **batch of 5-10 adjacent methodologies** from `QUEUE.txt` (each in its own worktree, full lifecycle). On every completion → dispatch one replacement batch.

## Main-thread rule: orchestration only

The parent agent NEVER does the actual work — no research, no file writes, no commits, no merges. Its job is purely:
- pop paths from `QUEUE.txt`
- dispatch worktree subagents
- record `DONE.txt`
- run `git pull` / `git push` for the bare repo
- delete the cron when queue drains

All research, all `agent-integration.md` writes, all `CHANGELOG.md` edits, all commits, and all `git merge --ff-only` into main happen **inside subagent worktrees** per `BRIEF.md`. If the parent finds itself reading a target README or editing a methodology file, it's doing the wrong thing — dispatch a batch instead.

Cron fires every 5 minutes as a safety net (tops up pool to 5 if the session has fewer live agents).

## State files (gitignored)

- `QUEUE.txt` — remaining methodology absolute paths (one per line).
- `DONE.txt` — audit log: `path<TAB>OK|SKIP|FAIL<TAB>iso-date`.
- `BRIEF.md` — committed subagent prompt template (batch mode).

## On completion notification (primary)

1. **Record.** For each path in the completed batch: append to `DONE.txt` as `<path>\tOK\t<iso-date>`. (Parent tracks which paths went to which agent.)

2. **Pull main:** `git -C <repo> pull --ff-only origin main`.

3. **Replacement dispatch.** If `QUEUE.txt` non-empty:
   - Take first **8 lines** (or all remaining if fewer) → `BATCH`.
   - `sed -i "1,8d" QUEUE.txt` (use actual count).
   - Skip already-enriched within the batch at agent level (agent handles it).
   - Launch Agent with `isolation: "worktree"`, prompt = `BRIEF.md` contents + `\n\nTARGETS:\n<path1>\n<path2>\n...\n`. `run_in_background: true`.

4. **Queue empty check.** If `QUEUE.txt` empty AND no active agents: push, `CronDelete` this cron, tell user research complete.

## On cron tick (safety net)

1. `git -C <repo> pull --ff-only origin main` — pick up agent merges.
2. Estimate active agents. If fewer than 5 active and queue non-empty, top up: dispatch `(5 - estimated_active)` batches of 8.
3. `git -C <repo> push` any local commits.
4. Report: `Cron tick: pool N. Queue M. Done K.`

## Why batches

- 5 agents × 8 targets/batch = **40 methodologies per tick cycle** (vs 5 previously).
- Fewer parent-agent turns, lower parent-context overhead.
- One commit per batch, one merge per batch — cleaner git history.
- Adjacent paths tend to share a domain, so the subagent can amortize research (related tools, same subagents).

## Batch sizing

- Default: 8 targets per batch.
- Tail case: if `< 8` remain in queue, batch = remaining.
- Never exceed 10 in a single batch — agent context gets too thin per methodology.

## Rerun from scratch

```bash
rm skills/faion/.research/QUEUE.txt skills/faion/.research/DONE.txt
bash skills/faion/.research/build-queue.sh
```

## Stop conditions

- Queue empty + no active agents → push, CronDelete, done.
- 3+ consecutive FAIL batches → pause, tell user, keep cron running but stop dispatching.
