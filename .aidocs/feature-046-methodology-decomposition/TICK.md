# TICK — feature-046 methodology decomposition

Self-replenishing pool of Sonnet subagents that decompose oversized methodologies (≥25KB) into smaller one-concept slugs.

## Configuration

| Param | Value | Notes |
|-------|-------|-------|
| `pool_size` | 5 | Sonnet quota; decomposition is heavier than migration |
| `batch_size` | 1 | Each oversized source needs full attention |
| `model` | `sonnet` | Needs semantic boundary detection |
| `tick_interval` | 5m | `/loop 5m` |
| `merge_lock` | `flock /tmp/faion-network-merge.lock` | Shared with feature-045 |

## State files (gitignored)

- `.aidocs/feature-046-methodology-decomposition/QUEUE.txt` — pending oversized absolute paths (114 at start)
- `.aidocs/feature-046-methodology-decomposition/DONE.txt` — `<old-slug>\tOK\t<N-new-slugs>\t<iso-date>\t<commit-list>`
- `.aidocs/feature-046-methodology-decomposition/FAILED.txt` — `<old-slug>\tFAIL\t<reason>\t<iso-date>`

## Tick prompt (drop into /loop 5m)

```
5m feature-046 decomposition tick. Pool=5, model=sonnet, batch=1.

Repo: /home/nero/workspace/projects/faion-net/faion-network
Source of truth: .aidocs/feature-046-methodology-decomposition/{BRIEF,TICK}.md (committed).
State (gitignored): .aidocs/feature-046-methodology-decomposition/{QUEUE,DONE,FAILED}.txt.

HARD RULE: parent does NOT do research/writes/commits/merges. Only: pop lines → dispatch agents → record outcomes → pull/push bare repo → delete cron when empty.

This tick:
1. cd /home/nero/workspace/projects/faion-net/faion-network. git pull --ff-only origin main.
2. Count active background agents from system reminders / TaskList.
3. If active < 5 AND .aidocs/feature-046-methodology-decomposition/QUEUE.txt non-empty: for each missing slot, head -1 .aidocs/feature-046-methodology-decomposition/QUEUE.txt → sed -i '1d' .aidocs/feature-046-methodology-decomposition/QUEUE.txt → dispatch Agent(general-purpose, model: "sonnet", isolation: "worktree", run_in_background: true) with prompt = "Read .aidocs/feature-046-methodology-decomposition/BRIEF.md and execute end-to-end for the source below. Mandatory pre-flight: also Read docs/skill-authoring.md, docs/methodology-xml-schema.md, docs/methodology-tag-glossary.xml, docs/examples/methodology-reference.xml. Use scripts/validate-methodology-xml.py on every new slug.\n\nCRITICAL: write files via worktree-relative paths (skills/...), never absolute /home/... — those leak into main.\n\nSOURCE:\n<absolute path>".
4. git push origin main.
5. Report ONE line: Tick: pool=N queue=M done=K active=A failed=F.

On completion notification: cd repo, git pull --ff-only, parse the agent's report (`batch=<old> done=<N> failed=<M>`), append result to .aidocs/feature-046-methodology-decomposition/DONE.txt or FAILED.txt, pop next line from QUEUE, dispatch replacement.

Stop conditions:
- Queue empty AND no active agents → git push, CronDelete this loop, final tally.
- 3+ "out of extra usage" failures → CronDelete, alert user, restore those paths to head of QUEUE.
- 5+ "not-oversized" reports — likely false positives; CronDelete, alert user.
- User says stop → CronDelete.

Never force-push, never --no-verify, no Co-Authored-By, no emojis.
```

## Stop conditions

- Queue empty + no active → push, `CronDelete <id>`, final tally
- 3+ quota errors → `CronDelete <id>`, restore paths to QUEUE head, alert user with quota info
- 5+ "not-oversized" reports → `CronDelete <id>`, alert (queue may need re-classification)
- User says stop → `CronDelete <id>`

## After feature-046 completes

- The 114 oversized are now N×~3 = ~350-500 new small methodologies, each ≤15K
- Append all new slugs to feature-045 QUEUE for migration (they're already in `methodology.xml` shape, so this is a no-op for them)
- Catalog regeneration runs to pick up new slugs
- feature-047 (router conversion) can begin
