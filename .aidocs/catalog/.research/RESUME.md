# Resume catalog orchestration (after /compact or session restart)

Last snapshot: 2026-04-25 — `done=723/1279` (57%), queue=21 batch tokens. Slot B (`a5b2537e78545e4ac`) still inflight at compact time — its `/tmp/cr-B.json` may land after session ends.

## What survives the session

Survives on disk (gitignored):
- CSV state: `.aidocs/catalog/data/{domains,methodologies}.csv` — canonical, rows with empty `description` are todo
- `.aidocs/catalog/.research/QUEUE.txt` — remaining batch tokens (one per line)
- `.aidocs/catalog/.research/DONE.txt` — append-only log of completed batches
- `.aidocs/catalog/.research/BRIEF.md` — subagent contract
- `.aidocs/catalog/.research/TICK.md` — orchestration rules
- `/tmp/cb-{A,B,C}.json` — last batch input files (may be stale)
- `/tmp/cr-{A,B,C}.json` — last batch result files (apply if newer than CSV)

Dies with session:
- Cron job (was ID `436aa92b`, every 5 min) — must reschedule
- Inflight async subagents — likely killed; if they finished before kill, results are in `/tmp/cr-*.json`

## Resumption protocol

```bash
cd /home/nero/workspace/projects/faion-net/faion-network

# 1. Recover any unapplied results from previous session
for s in A B C D E; do
  if [ -f /tmp/cr-$s.json ] && [ /tmp/cr-$s.json -nt .aidocs/catalog/data/methodologies.csv ]; then
    python3 .aidocs/catalog/scripts/catalog.py update /tmp/cr-$s.json
  fi
done

# 2. Check current state
python3 .aidocs/catalog/scripts/catalog.py status
# Expected: phase=methodologies done=N/1279 OR DONE
# If DONE → run render and exit
```

If `DONE`:
```bash
python3 .aidocs/catalog/scripts/catalog.py render
# Outputs: docs/catalog.md + docs/catalog.json
# Then: cleanup .research/, archive PLAN.md
```

If still in progress:

```bash
# 3. Pick 3 fresh disjoint slices
python3 .aidocs/catalog/scripts/catalog.py pick --skip 0  --size 25 --out /tmp/cb-A.json
python3 .aidocs/catalog/scripts/catalog.py pick --skip 25 --size 25 --out /tmp/cb-B.json
python3 .aidocs/catalog/scripts/catalog.py pick --skip 50 --size 25 --out /tmp/cb-C.json

# 4. Pop 3 tokens from QUEUE
sed -i '1,3d' .aidocs/catalog/.research/QUEUE.txt
```

5. Spawn 3 parallel async agents (model=haiku, run_in_background=true). Each prompt:
   ```
   Read /home/nero/workspace/projects/faion-net/faion-network/.aidocs/catalog/.research/BRIEF.md and follow it for batch file /tmp/cb-<SLOT>.json. Write result to /tmp/cr-<SLOT>.json. SLOT=<SLOT>.
   ```

6. Reschedule the cron tick (was every 5 min). Pattern: `*/5 * * * *`. Prompt: see "Cron tick prompt" below.

## Pool config

| Param | Value |
|-------|-------|
| pool_size | 3 |
| batch_size | 25 |
| model | haiku |
| slots | A, B, C |
| total methodologies | 1279 |
| total domains | 100 (already done) |

## Per-completion handler

When `<task-notification>` arrives for a slot:

```bash
python3 .aidocs/catalog/scripts/catalog.py update /tmp/cr-<slot>.json
token=$(head -1 .aidocs/catalog/.research/QUEUE.txt)
sed -i '1d' .aidocs/catalog/.research/QUEUE.txt
echo -e "<slot>\tOK\t$(date -Iseconds)\t$token" >> .aidocs/catalog/.research/DONE.txt
# Pick next slice — skip = (active_count_excluding_this_slot) * 25
python3 .aidocs/catalog/scripts/catalog.py pick --skip $((active * 25)) --size 25 --out /tmp/cb-<slot>.json
# Spawn replacement agent (same prompt as above)
```

## Cron tick prompt (reschedule on resume)

```
Catalog pool tick. Repo: /home/nero/workspace/projects/faion-net/faion-network. Source of truth: .aidocs/catalog/.research/TICK.md and BRIEF.md.

Steps:
1. cd repo
2. python3 .aidocs/catalog/scripts/catalog.py status. If "DONE": render, CronDelete this job, report and stop.
3. Count active background catalog agents.
4. While active < 3 AND .aidocs/catalog/.research/QUEUE.txt non-empty:
   a. Pop token from QUEUE.txt
   b. Pick free slot from {A,B,C}
   c. python3 .aidocs/catalog/scripts/catalog.py pick --skip $((active * 25)) --size 25 --out /tmp/cb-<slot>.json
   d. Spawn ONE general-purpose agent (model=haiku, run_in_background=true) with prompt:
      "Read /home/nero/workspace/projects/faion-net/faion-network/.aidocs/catalog/.research/BRIEF.md and follow it for batch file /tmp/cb-<slot>.json. Write result to /tmp/cr-<slot>.json. SLOT=<slot>."
   e. active += 1
5. Report: "Tick: pool=N queue=M done=K/1279"

Hard rule: parent never reads README files, never writes descriptions. Only orchestrates.
```

## Failure modes

- **Race: same key in two batches.** Update is idempotent — first apply wins, second sees non-empty and skips. Wasted work only.
- **Subagent stops early (e.g. 24/25).** Apply the partial result; the missing row stays pending and will be picked again next batch. No retry needed manually.
- **Quota error.** If 3+ agents fail with "out of extra usage": CronDelete, restore the 3 batch tokens to head of QUEUE.txt, alert user.
- **/tmp lost on reboot.** Re-run `pick` for fresh slices; lose only inflight agents' work (always re-pickable from CSV).

## Final cleanup (after DONE)

```bash
python3 .aidocs/catalog/scripts/catalog.py render  # docs/catalog.md + docs/catalog.json
# Optionally archive
mv .aidocs/catalog/.research .aidocs/catalog/.research.archive
```
