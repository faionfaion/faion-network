---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-02
version: 2.0.0
applies_to: any
---

# Poll-Agents Workflow

## Summary

Self-replenishing pool of N background subagents draining a queue of independent task batches. The parent does only orchestration (pop queue + dispatch + record); every write, commit, and merge happens inside isolated worktree subagents. The pool stays full via two complementary signals: a periodic cron tick (keepalive, drain detection, post-`/compact` recovery) and a per-completion handler (real-time one-per-completion replacement). On-disk state (`QUEUE.txt`, `DONE.txt`, optional `ACTIVE.txt`) makes the parent fully restartable.

## Why

Linear sequential processing of 100+ task batches is slow and burns parent context. A pool that keeps N subagents in flight, replaces one-per-completion, and persists state to disk turns parent latency into a constant overhead and lets throughput scale with quota and merge-lock capacity. Battle-tested at feature-045 (140 batches × 8 paths = 1142 methodologies enriched) and feature-048 (120 tier playbooks across 4 waves with strict 15-in-flight cap).

## When To Use

- ≥30 independent task batches that can run in parallel.
- Each batch is small (1-8 paths) and self-contained.
- Tasks must commit + push (worktree isolation prevents conflicts).
- Long queue that benefits from cron-tick keepalive across `/compact` boundaries.

## When NOT To Use

- &lt;30 batches — sequential execution is simpler and avoids the pool's fixed setup cost.
- Tasks share state or depend on each other.
- Tasks need to coordinate mid-execution.
- Single-feature SDD work — use `sdd-batch-orchestrator` instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | Core principle (parent isolation), role split, battle-tested examples, language convention. |
| `content/02-phases.xml` | Four phases: initialize state → initial dispatch → steady-state loop (cron tick + completion handler) → drain. |
| `content/03-state-shape.xml` | `QUEUE.txt`/`DONE.txt`/`ACTIVE.txt` + atomic `head/tail/mv` pop; why on-disk state survives `/compact`. |
| `content/04-replenishment.xml` | Two-signal pattern, strict 15-in-flight cap, quota gate, retry-with-sonnet on failure. |
| `content/05-anti-patterns.xml` | Parent doing writes, missing `flock`, polling instead of completion handler, in-memory state, over-commit, batched replacement. |

## Related

- `.aidocs/conventions/workflows/workflow-spec.md` — workflow authoring spec.
- `skills/faion/workflows/sdd-batch-orchestrator/` — SDD batch counterpart for single-feature or related-feature work.
- `skills/faion/workflows/AGENTS.md` — workflow index.
- `docs/methodology-tag-glossary.xml` — closed tag vocabulary used by `content/*.xml`.
