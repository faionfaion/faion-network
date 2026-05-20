---
status: active
audience: both
owner: ruslan
last_verified: 2026-05-07
version: 1.0.0
applies_to: any
content_id: 35c7522f4958fe07
success_criteria:
  - `.product/` on-disk layout (master-prompt, state, decisions, tasks, research) exists before any subagent runs.
  - Each phase advances only after its outputs land on disk and state.md records the transition.
  - Orchestrator dispatches subagents by file reference (path), never by inline prompt text.
  - Phase 6 validation passes before the run is declared production-ready.
---

# Idea-to-Prod Workflow

## Summary

Single-prompt autonomous build: from one idea sentence to a production-deployed system, driven by a cron tick (`*/5 * * * *`) and a fixed file layout (`master-prompt.md` + `state.md` + `decisions.md` + `tasks/` + `research/`). The orchestrator never carries heavy work — it dispatches subagents by file reference (path to master-prompt + path to task brief), reads the bounded summary, and updates `state.md`. Six phases run in order: research (parallel) → brainstorm → SDD plan → implement → deploy → validate. Each phase advances only when its outputs exist on disk and `state.md` reflects the transition.

## Why

Multi-week projects drift when the orchestrator improvises long prompts each tick: token cost balloons, context compactions lose state, and parallelism collapses. Encoding the project as an on-disk file layout (read by every subagent via `Read`, not pasted in prompts) makes the orchestrator restartable across compactions and cheap per tick. The cron tick is a heartbeat, not control flow — the orchestrator drives iterations continuously and wakes itself if missed. Sibling `/faion` workflows (`brainstorm`, `sdd-batch-orchestrator`, `improver`, `media-ops`) are invoked by name from the matching phase; this workflow is the umbrella shape that composes them.

## When To Use

- One-prompt asks like "build this end-to-end", "ідея до прод", "запусти проект сам", "автономний білд".
- Greenfield projects where the operator wants the loop to drive itself.
- Projects that need research → brainstorm → SDD → implement → deploy → validate inside one cron-driven session.
- Multi-day work that must survive context compaction and resume from disk state.

## When NOT To Use

- Single feature already specced — use `sdd-batch-orchestrator` directly.
- Pure ideation with no build intent — use `brainstorm` standalone.
- Session-end capture or audit — use `improver`.
- AI media outlet (TG channel + site) — use `media-ops` (more specialized).
- One-shot script or experiment with no SDD lifecycle — manual edit beats this overhead.

## Content

| File | What's inside |
|------|---------------|
| `content/00-routing.xml` | Auto-route triggers vs sibling workflows; consent gate; orchestrator vs operator vs subagent split. |
| `content/10-bootstrap.xml` | `.product/` directory layout; master-prompt, state, decisions, tasks, research file contracts. |
| `content/20-phases.xml` | Six phases (research, brainstorm, plan, implement, deploy, validate); advance condition; sibling-workflow invocation. |
| `content/30-token-discipline.xml` | File-reference dispatch, background mode, subagent summary cap, no-narration rule. |
| `content/40-cron-loop.xml` | `*/5 * * * *` tick semantics; heartbeat not control; restart-from-disk; one-line state log. |
| `content/50-failure-modes.xml` | Recovery table: failed subagent, dead-end fallback, internet chain, quota check, open question parking, hook failure. |
| `content/60-stop-conditions.xml` | Operator halt, irreversible action gate, phase-6 pass, cron expiry. |
| `decisions.xml` | Why on-disk file layout, cron-as-heartbeat, file-ref dispatch, sibling-workflow composition, append-only decisions. |

## Related

- `../brainstorm/` — Phase 2 invocation target.
- `../sdd-batch-orchestrator/` — Phase 3-4 invocation target.
- `../improver/` — post-validation session capture.
- `../media-ops/` — alternative for AI media pipeline.
- `../poll-agents/` — alternative for queue-driven batch work.
- `docs/skill-authoring.md` — folder shape and token budgets.
