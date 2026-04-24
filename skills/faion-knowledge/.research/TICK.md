# Research Tick — Always-5-Active Dispatch

**Policy:** keep 5 subagents concurrently active at all times. Each completion → dispatch one replacement from `QUEUE.txt`.

Two entry paths trigger this workflow:
1. **Cron tick** (`*/5 * * * *`) — safety net: top up pool to 5 if the session has fewer live agents (e.g. after a stall).
2. **`<task-notification>` completion** — primary signal: on every agent-complete, immediately dispatch 1 replacement.

## State files (gitignored)

- `QUEUE.txt` — remaining methodology absolute paths.
- `DONE.txt` — audit log: `path<TAB>WROTE|SKIP|FAIL<TAB>iso-date`.
- `BRIEF.md` — committed subagent prompt template.

## On completion notification (primary)

1. **Record.** Append to `DONE.txt`:
   `<target-path>\tWROTE\t<iso-date>`

2. **Commit gate.** `git status --short skills/faion-knowledge/knowledge | grep agent-integration.md | wc -l`. If ≥ 5 new files:
   - Update `CHANGELOG.md` `## [Unreleased]` `### Changed` with `- Research: enriched N more methodologies with agent-integration.md`
   - `git add skills/faion-knowledge/knowledge/ CHANGELOG.md`
   - Commit: `research: enrich N methodologies with agent-integration.md`
   - Push every 3rd commit.

3. **Replacement dispatch.** If `QUEUE.txt` non-empty:
   - Take first line → `TARGET`, `sed -i '1d' QUEUE.txt`.
   - If `<TARGET>/agent-integration.md` already exists: append `SKIP` to `DONE.txt`, loop to next queue line (up to 10 skips, then give up this round).
   - Launch one `general-purpose` Agent with `BRIEF.md` + `Target: <TARGET>` as prompt, `run_in_background: true`.

4. **Queue empty check.** If `QUEUE.txt` empty AND no active agents: final commit/push, `CronDelete` this cron, tell user research complete.

## On cron tick (safety net)

1. Count new `agent-integration.md` files since last commit.
2. Count "active agents" = recent Agent tool calls without completion notifications in this turn (heuristic: assume missing = still running).
3. **If fewer than 5 believed active**, top up: dispatch `(5 - estimated_active)` replacements from `QUEUE.txt` using the same BRIEF + Target pattern.
4. Run commit gate (step 2 above).
5. Report: `Cron tick: topped up pool by N. Queue: M. Done: K.`

## Rules

- **Drop queue lines immediately on dispatch** (before the agent returns) to prevent collision if a cron tick fires while a completion notification is being handled.
- **Never exceed 5 concurrent agents.** If unsure, err low — a cron tick will top up.
- **Commit in batches of 5**, push every 3 commits.

## Rerun from scratch

```bash
rm skills/faion-knowledge/.research/QUEUE.txt skills/faion-knowledge/.research/DONE.txt
bash skills/faion-knowledge/.research/build-queue.sh
```

## Stop conditions

- Queue empty + no active agents → CronDelete, done.
- 3+ consecutive agent failures → pause, tell user, keep cron running but stop dispatching new agents until user says go.
