# Research Tick — Per-Cron Workflow

Run every 5 minutes. One tick = dispatch **5 parallel subagents**, each researching one methodology.

## Inputs (state files, gitignored)

- `QUEUE.txt` — remaining methodology absolute paths (one per line). Built once by `build-queue.sh`.
- `DONE.txt` — completed methodology paths (append-only audit).
- `BRIEF.md` — committed subagent prompt template.

## Tick procedure

1. **Queue check.** If `QUEUE.txt` is missing or empty:
   - If missing → run `bash skills/faion-knowledge/.research/build-queue.sh` then continue.
   - If empty → research complete. Report to user, `CronList` + `CronDelete` this cron, and stop.

2. **Pick next 5 methodologies.** Read first 5 lines of `QUEUE.txt` → `TARGET_PATHS` (array). If fewer than 5 remain, take what's left.

3. **Skip already-enriched.** For each target, if `<TARGET_PATH>/agent-integration.md` already exists, append to `DONE.txt` with marker `SKIP` and omit from dispatch.

4. **Drop picked lines from QUEUE.txt IMMEDIATELY** (before dispatch) to avoid collision with concurrent ticks or prior still-running agents:
   `sed -i "1,5d" skills/faion-knowledge/.research/QUEUE.txt` (use actual count if <5).

5. **Dispatch 5 general-purpose Agents IN PARALLEL** (single message, multiple Agent tool calls):
   - Each: `description`: `Research methodology: <basename>`, `subagent_type`: `general-purpose`
   - Each: `prompt` = full contents of `BRIEF.md` + final line `Target: <TARGET_PATH>`
   - Launch async (tool returns immediately); rely on completion notifications, or SendMessage to check, but do NOT block this tick.

6. **This tick ends after dispatch.** Completion notifications arrive as the agents finish. When each one completes:
   - Append `TARGET_PATH\tWROTE\t<date-iso>` to `DONE.txt`.
   - Count new `agent-integration.md` files since last commit. If ≥ 5:
     - `git add skills/faion-knowledge/knowledge/ CHANGELOG.md`
     - Update `CHANGELOG.md` under `## [Unreleased]` `### Changed` with `- Research: enriched N methodologies`
     - Commit: `research: add agent-integration.md for N methodologies (round R)`
     - Push every 3rd commit.

7. **Report to user after dispatch** (one line):
   `Tick R: launched 5 agents (<basename-list>). Queue remaining: N. Done total: M.`

## Stop conditions

- Queue empty → complete, delete cron.
- 3+ consecutive agent failures → pause, tell user, keep cron paused (await guidance).

## Rerun

```bash
rm skills/faion-knowledge/.research/QUEUE.txt skills/faion-knowledge/.research/DONE.txt
bash skills/faion-knowledge/.research/build-queue.sh
```
