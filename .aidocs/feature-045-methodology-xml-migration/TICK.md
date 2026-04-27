# Tick — feature-045 methodology XML migration pool

Orchestration rules for the parent thread driving the migration pool. Pattern: `/faion-poll-agents`.

**Pool size:** 10
**Model:** haiku
**Subagent type:** general-purpose
**Repo:** `/home/nero/workspace/projects/faion-net/faion-network`
**State home:** `.aidocs/feature-045-methodology-xml-migration/`

## Files

| File | Purpose | Tracked? |
|------|---------|----------|
| `BRIEF.md` | Subagent instructions | YES (committed) |
| `TICK.md` | This file | YES |
| `QUEUE.txt` | Pending batches — one absolute folder path per line | NO (gitignore) |
| `DONE.txt` | Tab-separated `<path>\tOK\t<iso-date>\t<commit-sha>` | NO |

## Hard rule for parent

Parent does NOT migrate / write XML / commit. Only:
- pop lines from `QUEUE.txt`
- dispatch background subagents
- record outcomes to `DONE.txt`
- pull / push the bare repo
- delete the cron when queue empty
- restore failed batches on quota exhaustion

If parent starts editing methodology files, abstraction is broken — STOP and re-delegate.

## Tick — each fire

### 1. cd repo + pull

```bash
cd /home/nero/workspace/projects/faion-net/faion-network
git pull --ff-only origin main
```

### 2. Count active background agents

Track dispatched IDs in conversation. From system reminders count active.

### 3. If active < 10 AND QUEUE non-empty: dispatch replacements

For each missing slot:

1. `head -3 .aidocs/feature-045-methodology-xml-migration/QUEUE.txt` — read next batch (3 paths).
2. `sed -i '1,3d' .aidocs/feature-045-methodology-xml-migration/QUEUE.txt` — pop atomically.
3. Dispatch:

```
Agent({
  subagent_type: "general-purpose",
  model: "haiku",
  isolation: "worktree",
  run_in_background: true,
  description: "f045 batch: <slug-1>+<slug-2>+<slug-3>",
  prompt: "Read .aidocs/feature-045-methodology-xml-migration/BRIEF.md and execute it end-to-end for the methodology folders below.\n\nCRITICAL: write files via worktree-relative paths (skills/...), never absolute /home/... — those leak into main.\n\nFOLDERS:\n<path-1>\n<path-2>\n<path-3>"
})
```

### 4. Push

```bash
git push origin main
```

### 5. One-line report

```
Tick: pool=N queue=M done=K active=A failed=F
```

## Completion handler (per task-notification)

1. `cd repo; git pull --ff-only`
2. Append batch lines to `DONE.txt` with status + sha from latest commits.
3. Pop next batch from `QUEUE.txt`, dispatch replacement.
4. One-line: `Pool=N: <prev-id> done(<n>/<batch>), replacement <new-id> dispatched. Queue=M done=K.`

## Stop conditions

- **Queue empty + no active agents** → `git push`, `CronDelete <id>`, run final `python3 scripts/validate-methodology-xml.py --all`, report final tally.
- **3+ "out of extra usage" failures in a window** → `CronDelete <id>`, restore failed batches to head of `QUEUE.txt`, alert user.
- **3+ validation failures from same agent** → mark batch failed, restore to QUEUE for human review.
- **User says stop** → `CronDelete <id>`, leave queue and worktrees as-is.

## Concurrent merge

Subagents serialize ff-only merges via `flock /tmp/faion-network-merge.lock`. Parent does NOT need the lock for read-only `git pull --ff-only`.

## CHANGELOG conflicts

Pre-commit hook requires CHANGELOG entry under `## [Unreleased]`. Concurrent batches edit the same section — resolution: subagent rebases, keeps both entries, re-stages, retries.

## Reporting cadence

- Per dispatch / completion: ONE line.
- Per tick: ONE line.
- Per stop: ONE line summary.

## Tick prompt (for /loop 5m)

```
feature-045 methodology XML migration tick. Pool=10, model=haiku.

Repo: /home/nero/workspace/projects/faion-net/faion-network
Source of truth: .aidocs/feature-045-methodology-xml-migration/TICK.md + BRIEF.md (committed).
State (gitignored): .aidocs/feature-045-methodology-xml-migration/QUEUE.txt, DONE.txt.

HARD RULE: parent does NOT migrate/write/commit/merge. Only: pop batches → dispatch agents → record DONE → pull/push bare repo → delete cron when empty.

This tick:
1. cd /home/nero/workspace/projects/faion-net/faion-network. git pull --ff-only origin main.
2. Count active background agents from system reminders.
3. If active < 10 AND .aidocs/feature-045-methodology-xml-migration/QUEUE.txt non-empty: for each missing slot, head -3 .aidocs/feature-045-methodology-xml-migration/QUEUE.txt → sed -i '1,3d' that file → dispatch Agent(general-purpose, model: "haiku", isolation: "worktree", run_in_background: true) with prompt = "Read .aidocs/feature-045-methodology-xml-migration/BRIEF.md and execute it end-to-end for the methodology folders below.\n\nCRITICAL: write files via worktree-relative paths (skills/...), never absolute /home/... — those leak into main.\n\nFOLDERS:\n<batch-3-paths>".
4. git push origin main.
5. Report: Tick: pool=N queue=M done=K active=A failed=F.

On completion notification: cd repo, git pull, append <path>\tOK\t<iso>\t<sha> per migrated folder to DONE.txt, pop next batch, dispatch replacement.

Stop: queue empty AND no active → git push, CronDelete this loop, final tally + run scripts/validate-methodology-xml.py --all.

If 3+ batches return "out of extra usage" → CronDelete, alert user, restore those batches to head of QUEUE.txt.

Never force-push, never --no-verify, no Co-Authored-By, no emojis.
```

## Pilot phase

**Before mass dispatch:** run pilot of 10 batches (≈30 methodologies) covering a mix of tier/group:

- 3 batches old shape from `solo/dev/automation-tooling/`
- 3 batches old shape from `pro/`
- 2 batches new shape from `geek/sdlc-ai/`
- 2 batches new shape from `geek/ai/ai-agents/`

After pilot: human reviews validator output + spot-checks 5 random files for content fidelity. If quality acceptable, scale to full queue.

## Queue construction

```bash
# all methodology folders that still have a body file:
find skills/faion/knowledge -mindepth 4 -maxdepth 4 -type d \
  | while read d; do
      if [ -f "$d/README.md" ] || [ -f "$d/AGENTS.md" ] || [ -f "$d/agent-integration.md" ]; then
        echo "$(realpath "$d")"
      fi
    done > .aidocs/feature-045-methodology-xml-migration/QUEUE.txt
```

Expected size: ~1140 paths, ~380 batches at batch=3.
