# Research Subsystem — agent-integration.md enrichment

Enriches every methodology under `skills/faion-knowledge/knowledge/` with an `agent-integration.md` file covering: when to use / when NOT to use / failure modes / agentic workflow / CLI tools / services / templates / best practices.

## Files

| File | Role | Committed? |
|------|------|-----------|
| `BRIEF.md` | Subagent research prompt template | yes |
| `TICK.md` | Per-cron-fire tick workflow | yes |
| `build-queue.sh` | Builds `QUEUE.txt` from filesystem | yes |
| `README.md` | This file | yes |
| `.gitignore` | Ignores runtime state | yes |
| `QUEUE.txt` | Remaining methodology paths | no (gitignored) |
| `DONE.txt` | Completed paths audit log | no (gitignored) |

## Flow

1. Cron fires every 5 minutes with prompt `Follow skills/faion-knowledge/.research/TICK.md ...`
2. Tick reads first line of `QUEUE.txt`, dispatches one general-purpose Agent with `BRIEF.md`, agent writes `agent-integration.md` into the methodology dir.
3. State moves from QUEUE → DONE. Every 3 enrichments, commit + push.
4. Queue empty → CronDelete, report complete.

## Rerun from scratch

```bash
rm skills/faion-knowledge/.research/QUEUE.txt skills/faion-knowledge/.research/DONE.txt
bash skills/faion-knowledge/.research/build-queue.sh
# Then /loop 5m with the TICK.md prompt, or schedule via CronCreate manually.
```

## Output format

Each methodology gains a new sibling file `agent-integration.md` with a fixed skeleton — see `BRIEF.md` for the exact structure.
