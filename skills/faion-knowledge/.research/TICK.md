# Research Tick — Always-5-Active Worktree Dispatch

**Policy:** keep 5 subagents concurrently active. Each agent runs in its own git worktree and ships the full lifecycle (research → edit → commit → merge-to-main). On every completion → dispatch one replacement.

Cron fires every 5 minutes as a safety net (tops up pool to 5 if the session has fewer live agents).

## State files (gitignored)

- `QUEUE.txt` — remaining methodology absolute paths (one per line).
- `DONE.txt` — audit log: `path<TAB>OK|SKIP|FAIL<TAB>iso-date`.
- `BRIEF.md` — committed subagent prompt template. Agents do research+commit+merge themselves.

## On completion notification (primary)

1. **Parse summary line** from the returned result. Expected formats:
   - `OK <slug> — agent-integration.md (N lines), merged to main` → success
   - `FAIL <slug> — <reason>` → failure

2. **Record** to `DONE.txt`: `<target-path>\tOK|FAIL\t<iso-date>`.

3. **Pull main** (agent merged into the shared `.git` but our working copy may be stale):
   `git -C <repo> pull --ff-only || true` (no-op if already up to date; fails loudly if main diverged).

4. **Replacement dispatch.** If `QUEUE.txt` non-empty:
   - Take first line → `TARGET`, `sed -i '1d' QUEUE.txt`.
   - If `<TARGET>/agent-integration.md` already exists: append `SKIP` to DONE, loop to next queue line (up to 10 skips, then stop this round).
   - **Launch Agent with `isolation: "worktree"`** and prompt = `BRIEF.md` contents + `\n\nTarget: <TARGET>`. `run_in_background: true`.

5. **Queue empty check.** If `QUEUE.txt` is empty AND no active agents remain:
   - Push final state: `git push`.
   - `CronDelete <this-cron-id>`.
   - Report to user: `Research complete. N methodologies enriched.`

## On cron tick (safety net)

1. `git -C <repo> pull --ff-only` to pick up any agent merges.
2. Estimate active agents (heuristic: count of Agent tool calls dispatched this session without a completion notification yet).
3. If fewer than 5 active and `QUEUE.txt` non-empty, top up: dispatch `(5 - estimated_active)` agents, each with `isolation: "worktree"`.
4. Push any local commits we accumulated (`git -C <repo> push`).
5. Report: `Cron tick: topped up by N. Queue: M. Done: K.`

## Why worktree + agent-driven merge

- **Concurrency-safe.** Agents never trip on each other's working dirs. Each has its own worktree.
- **Serialized merges.** Agents merge via `flock /tmp/faion-research-merge.lock` — one merge at a time.
- **ff-only + rebase fallback.** Agent rebases onto latest main if needed. No force-push ever.
- **Pre-commit hook runs.** CHANGELOG.md check passes because each agent updates it.

## Rerun from scratch

```bash
rm skills/faion-knowledge/.research/QUEUE.txt skills/faion-knowledge/.research/DONE.txt
bash skills/faion-knowledge/.research/build-queue.sh
```

## Stop conditions

- Queue empty + no active agents → push, CronDelete, done.
- 3+ consecutive FAIL results → pause, tell user, keep cron running but stop new dispatches.
