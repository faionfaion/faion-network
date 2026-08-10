# Orchestration doctrine (token discipline for fan-out work)

Distilled from the faion `idea-to-prod` token-discipline rules. Any skill that spawns subagents
to do batch or long-running work should follow these. They are why a thin orchestrator can drive
dozens of items across a multi-day run without its context ballooning or collapsing at compaction.

## 1. File-reference dispatch — pass paths, not text

The orchestrator dispatches subagents **by file reference**: the prompt carries the path to a
contract (e.g. `worker.md`) plus a handful of identifiers (slug, phase, pool dir), never the
inlined content of large specs, manifests, or screenshots.

- **Why:** inlining a 14k-word spec into every spawn multiplies token cost by the fan-out width
  and re-pays it on every tick. A path is ~30 tokens; the worker `Read`s only what it needs.
- **How to apply:** keep shared context on disk (`meta.txt`, manifest files, `dag.json`). The
  worker opens them itself. The orchestrator's prompt to a worker should fit in a dozen lines.

## 2. Thin orchestrator — state on disk, not in context

The orchestrator carries **no heavy state in its head**. Everything needed to decide "what runs
next" is reconstructable from marker files (`phase-*.done/.in-flight/.failed/.awaiting`).

- **Why:** a multi-day run will be compacted, maybe across sessions. If progress lives only in
  conversation context, compaction loses it and parallelism collapses. On disk, recovery is just
  "tick again."
- **How to apply:** never track "which items are done" in prose — `dispatch.py` derives it. After
  a crash or compaction, re-run dispatch; the only manual cleanup is stale `.in-flight` markers
  for workers that truly died.

## 3. Bounded worker reports — return data, not essays

A worker's final message is **input for the orchestrator**, not a human-facing write-up. Cap it
(≈8 lines): phase, slug, outcome, output path(s), and anything the next step or the human must
know.

- **Why:** the orchestrator reads every worker's reply each tick. Verbose replies bloat the
  orchestrator's context — the exact thing thin-orchestration is protecting.
- **How to apply:** the artifact goes to a file (`out/<slug>/...`); the reply just points at it
  and flags blockers.

## 4. Gate before you spawn — quota + heartbeat

Before each wave, check headroom (`quota-gate` skill). Pause on HOLD; the loop stays alive and
resumes when capacity returns. Drive ticks off completion notifications, not a busy timer; use a
long `ScheduleWakeup` only as a backstop in case a worker hangs.

- **Why:** an ungated fan-out can burn the weekly ceiling in one run and lock out work for days.
  A busy-poll wakeup wastes tokens and warms-then-loses the prompt cache.
- **How to apply:** see `quota-gate/SKILL.md` and `pool-orchestrator/SKILL.md` step 5.
