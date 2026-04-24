# Research Tick — Per-Cron Workflow

Run every 5 minutes. One tick = research ONE methodology (or a small batch if queue is short).

## Inputs (state files, gitignored)

- `QUEUE.txt` — remaining methodology absolute paths (one per line). Built once by `build-queue.sh`.
- `DONE.txt` — completed methodology paths (append-only audit).
- `BRIEF.md` — committed subagent prompt template.

## Tick procedure

1. **Queue check.** If `QUEUE.txt` is missing or empty:
   - If missing → run `bash skills/faion-knowledge/.research/build-queue.sh` then continue.
   - If empty → research complete. Report to user, `CronList` + `CronDelete` this cron, and stop.

2. **Pick next methodology.** Read first line of `QUEUE.txt` → `TARGET_PATH`.

3. **Skip if already enriched.** If `<TARGET_PATH>/agent-integration.md` already exists, append path to `DONE.txt`, drop line 1 of `QUEUE.txt`, and go to step 7 (commit gate).

4. **Dispatch ONE general-purpose Agent** with:
   - `description`: `Research methodology: <basename>`
   - `subagent_type`: `general-purpose`
   - `prompt`: the full contents of `BRIEF.md` + a final line: `Target: <TARGET_PATH>`

5. **Wait for agent completion.** Agent writes `<TARGET_PATH>/agent-integration.md` and returns a one-line summary.

6. **Update state.**
   - Append `TARGET_PATH\tWROTE\t<date-iso>` to `DONE.txt`.
   - Drop line 1 of `QUEUE.txt`: `sed -i '1d' skills/faion-knowledge/.research/QUEUE.txt`.

7. **Commit gate.** Count new `agent-integration.md` files since last commit (`git status --short skills/faion-knowledge/knowledge | grep agent-integration.md | wc -l`). If ≥ 3:
   - `git add skills/faion-knowledge/knowledge/ CHANGELOG.md`
   - Update `CHANGELOG.md` under `## [Unreleased]` with `- Research: enriched <N> methodologies with agent-integration.md`
   - Commit: `research: add agent-integration.md for <N> methodologies (round <R>)`
   - Push every 5th commit.

8. **Report to user** (one line):
   `Tick <R>: <path-basename> → <agent-integration-lines> lines. Queue: <remaining>. Done: <total-done>.`

## Stop conditions

- Queue empty → complete, delete cron.
- 3 consecutive agent failures → pause, tell user, do not delete cron (await guidance).

## Rerun

To restart from scratch:
```bash
rm skills/faion-knowledge/.research/QUEUE.txt skills/faion-knowledge/.research/DONE.txt
bash skills/faion-knowledge/.research/build-queue.sh
```

To skip methodologies already enriched on a rebuild: `build-queue.sh` filters out any dir that already has `agent-integration.md`.
