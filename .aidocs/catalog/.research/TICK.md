# Tick handler — faion-network catalog pool

Repo: `/home/nero/workspace/projects/faion-net/faion-network`

Source of truth:
- CSV state: `.aidocs/catalog/data/methodologies.csv` + `domains.csv` (description filled = done)
- Disk state: `.aidocs/catalog/.research/QUEUE.txt` (batch tokens, one per line) + `DONE.txt` (tab-separated log)
- Subagent contract: `.aidocs/catalog/.research/BRIEF.md`

## Configuration

- pool_size = **5**
- batch_size = **25** rows per agent
- model = **haiku**
- slot tags = A, B, C, D, E

## Hard rule

Parent ONLY: pop QUEUE → pick CSV slice → dispatch agent → on completion apply `/tmp/cr-<slot>.json` via `catalog.py update` → record to DONE.txt → repeat.

Parent never reads README files itself, never writes descriptions, never edits the CSV by hand.

## Per-tick steps

1. `cd /home/nero/workspace/projects/faion-net/faion-network`
2. Run `python3 .aidocs/catalog/scripts/catalog.py status`. If output is `DONE` → cleanup (CronDelete + remove QUEUE.txt). Stop.
3. Count active background catalog agents (those whose `cr-<slot>.json` has not yet been applied).
4. While `active < 5` AND QUEUE.txt non-empty:
   a. Pop first line from QUEUE.txt: `head -1 QUEUE.txt` → batch token, then `sed -i '1d' QUEUE.txt`
   b. Choose a free slot (A/B/C/D/E — one not currently inflight)
   c. Pick CSV slice: `python3 .aidocs/catalog/scripts/catalog.py pick --skip $((active * 25)) --size 25 --out /tmp/cb-<slot>.json`
   d. Dispatch background Agent with prompt:
      `Read /home/nero/workspace/projects/faion-net/faion-network/.aidocs/catalog/.research/BRIEF.md and follow it for batch file /tmp/cb-<slot>.json. Write result to /tmp/cr-<slot>.json. SLOT=<slot>.`
   e. Increment active counter
5. Report one line: `Tick: pool=N queue=M done=K/1279`

## Per-completion steps (handler fires on `<task-notification>`)

1. `cd repo`
2. `python3 .aidocs/catalog/scripts/catalog.py update /tmp/cr-<slot>.json`
3. Append to DONE.txt: `<slot>\tOK\t<iso-date>\t<key-count>`
4. If queue non-empty AND active < 5: dispatch replacement (same as tick step 4).
5. Report one line: `Pool=N: <slot> done +25, queue=M done=K/1279`

## Stop conditions

- `catalog.py status` returns `DONE` → CronDelete + final render.
- Three consecutive subagent failures (out-of-quota / format error) → CronDelete, alert user, restore those slot tokens to head of QUEUE.txt.
- User says stop → CronDelete.

## Quota fallback

If subagent returns "out of extra usage" or quota error: do NOT silently retry. Restore the slot's batch token to head of QUEUE.txt, halt the cron, alert user.

## Final cleanup

After `DONE` reached:
1. `python3 .aidocs/catalog/scripts/catalog.py render` → produces `docs/catalog.md` + `docs/catalog.json`
2. CronDelete the loop job
3. Report: `Catalog complete: 100 domains + 1279 methodologies. Output: docs/catalog.md (NN KB), docs/catalog.json (NN KB).`
