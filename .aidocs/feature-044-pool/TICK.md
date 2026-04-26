# Tick — feature-044 pool

Orchestration rules for the parent thread driving the /faion-poll-agents pool for feature-044.

**Pool size:** 10
**Model:** opus (per user preference: always-opus)
**Subagent type:** general-purpose
**Repo:** `/home/nero/workspace/projects/faion-net/faion-network`
**State home:** `.aidocs/feature-044-pool/`

## Files (state on disk)

| File | Purpose | Tracked? |
|------|---------|----------|
| `BRIEF.md` | Subagent instructions | YES (committed) |
| `TICK.md` | This file | YES |
| `QUEUE.txt` | Pending batch lines `<domain>:<category>:<count>` | NO (.gitignore) |
| `DONE.txt` | Tab-separated `<line>\tOK\t<iso-date>\t<commit-sha>` | NO |

## Hard rule for parent (orchestrator)

The parent thread does NOT do research / writes / commits / merges. Only:

- pop lines off `QUEUE.txt`
- dispatch background `Agent` subagents
- record outcomes to `DONE.txt`
- pull / push the bare repo
- delete the cron when queue empty
- restore failed batches on quota exhaustion

If parent starts editing methodology files, the abstraction is broken — STOP and re-delegate.

## Each tick — do this:

### 1. cd repo + pull

```bash
cd /home/nero/workspace/projects/faion-net/faion-network
git pull --ff-only origin main
```

### 2. Count active background agents

Track dispatched agent IDs in conversation. If `<system-reminder>` lists active agents, count them; otherwise re-derive from in-memory state.

### 3. If active < 10 AND QUEUE non-empty: dispatch replacements

For each missing slot:

1. `head -1 .aidocs/feature-044-pool/QUEUE.txt` to read next line.
2. `sed -i '1d' .aidocs/feature-044-pool/QUEUE.txt` to pop atomically.
3. Dispatch:

```
Agent({
  subagent_type: "general-purpose",
  model: "opus",
  isolation: "worktree",
  run_in_background: true,
  description: "f044 batch: <line>",
  prompt: "Read .aidocs/feature-044-pool/BRIEF.md and execute it end-to-end for the batch line below.\n\nCRITICAL: write files via worktree-relative paths (skills/...), never absolute /home/... — those leak into main.\n\nBATCH: <line>"
})
```

### 4. Push

```bash
git push origin main
```

### 5. One-line report

```
Tick: pool=N queue=M done=K active=A
```

## Completion handler (per task-notification)

1. `cd repo; git pull --ff-only`
2. Read commit info — extract domain, count, category from latest commit message
3. Append to `DONE.txt`:
   ```
   <line>\tOK\t<iso-date>\t<commit-sha>
   ```
4. Pop next line from `QUEUE.txt`, dispatch replacement (same as step 3 above)
5. One-line report:
   ```
   Pool=N: <prev-id> done, replacement <new-id> dispatched. Queue=M done=K.
   ```

## Stop conditions

- **Queue empty + no active agents** → `git push`, `CronDelete <id>`, report final tally
- **3+ "out of extra usage" failures in a window** → `CronDelete <id>`, restore those lines to head of `QUEUE.txt`, alert user with quota info
- **User says stop** → `CronDelete <id>`, leave queue and worktrees as-is

## Cron drift recovery

After `/compact` or session restart, parent loses agent IDs. Tick reads `git log` and `QUEUE.txt`/`DONE.txt`, not in-memory state. Worst case: one duplicate cycle if a previous tick didn't commit.

## Concurrent merge

Subagents serialize ff-only merges via `flock /tmp/faion-network-merge.lock`. Parent does NOT need the lock for read-only `git pull --ff-only`.

## CHANGELOG conflicts

Pre-commit hook requires CHANGELOG entry under `## [Unreleased]`. Concurrent batches edit the same section. Resolution: subagent rebases, keeps both entries, re-stages, retries.

## Reporting cadence

- Per dispatch / completion: ONE line.
- Per tick: ONE line.
- Per stop: ONE line summary.

No per-file recap.

## Tick prompt (for /loop 5m)

```
feature-044 pool tick. Pool=10, model=opus.

Repo: /home/nero/workspace/projects/faion-net/faion-network
Source of truth: .aidocs/feature-044-pool/TICK.md + BRIEF.md (committed).
State (gitignored): .aidocs/feature-044-pool/QUEUE.txt, DONE.txt.

HARD RULE: parent does NOT do research/writes/commits/merges. Only: pop lines → dispatch agents → record DONE → pull/push bare repo → delete cron when empty.

This tick:
1. cd /home/nero/workspace/projects/faion-net/faion-network. git pull --ff-only origin main.
2. Count active background agents from system reminders.
3. If active < 10 AND QUEUE non-empty: for each missing slot, head -1 .aidocs/feature-044-pool/QUEUE.txt → sed -i '1d' that file → dispatch Agent(general-purpose, model: "opus", isolation: "worktree", run_in_background: true) with prompt = "Read .aidocs/feature-044-pool/BRIEF.md and execute it end-to-end for the batch below.\n\nCRITICAL: write files via worktree-relative paths, never absolute — those leak into main.\n\nBATCH: <line>".
4. git push origin main.
5. Report: Tick: pool=N queue=M done=K.

On completion notification: cd repo, git pull, append <line>\tOK\t<iso>\t<sha> to DONE.txt, pop next line, dispatch replacement.

Stop: queue empty AND no active → git push, CronDelete this job, final tally.

If 3+ batches return "out of extra usage" → CronDelete, alert user, restore those lines to head of QUEUE.txt.

Never force-push, never --no-verify.
```
