# Placement — Orchestration Frameworks
**Slice:** LangGraph, CrewAI, AutoGen/AG2, OpenAI Agents SDK, Google ADK, Claude subagents, checkpoint/rollback · **Author pass:** 5 of 10 · **Date:** 2026-08-04

## Already covered — do not duplicate

| Approach | Existing slug | Gap |
|---|---|---|
| Framework choice | `ai-agent-patterns` | Five frameworks as interchangeable targets; no runtime constraint, no dates. Stale, not missing |
| Multi-agent spec → framework | `multi-agent-basics` | Same; still names AutoGen (maintenance since 2025-10) |
| Crew/Flow shapes | `multi-agent-design-patterns` (8), `agent-patterns`, four `multi-agent-*` runners | None. CrewAI is sugar over patterns we publish |
| `output_pydantic` retry | `structured-output-mode-picker`, `strict-mode-required-fields` | None |
| Handoff payload, topology | `handoff-id-payload`, `multi-agent-orchestration-decision-tree` | First/last-agent-only guardrail scope |
| Subagent isolation, fan-out cost | `subagent-as-context-firewall`, `stream-json-orchestration`, `poll-agents` | #29966 → cost models understate |
| Deterministic replay | `agent-replay-harness-cookbook` | Reproduces a failure; does not resume a live run |
| Reverting an agent release | `agent-rollback-button-design` | Reverts a *release*, not run-level truncate-and-requeue |
| CLI as tool for foreign stacks | `faion-cli-agent-adapter-pattern` | No A2A row |

**Genuinely uncovered:** the on-disk checkpoint ledger for a bash/cron orchestrator — identity-checked-before-write, in-flight marker before dispatch, per-unit append-only history, rollback as truncate + requeue. Zero slugs across 23 domains.

## Verdict summary

| Approach | Verdict | Decision | Target |
|---|---|---|---|
| LangGraph | 🟡 | Idea → new methodology + poll-agents edits; dated constraint note | `on-disk-checkpoint-ledger`, `ai-agent-patterns` |
| CrewAI | 🔴 | Staleness line | `ai-agent-patterns` |
| AutoGen/AG2/MS AF | 🔴 | Fracture footnote | `multi-agent-basics`, `-conversational` |
| OpenAI Agents SDK | 🔴 | Guardrail caution | `handoff-id-payload`, `multi-agent-orchestration-decision-tree` |
| Google ADK / A2A | 🟡 | A2A row | `faion-cli-agent-adapter-pattern` |
| Claude subagents | 🟢 baseline | #29966 rewrites fan-out + quota guidance | `poll-agents/content/04`, `/05` |
| Checkpoint/rollback | 🟢 | New methodology + both orchestrators | below |

## Workflow changes

Workflows are **not** in `tier-manifest.json` (verified: 0 of 3078 entries under `skills/faion/workflows/`). Registration = `catalog.json` only.

**`poll-agents/content/03-state-shape.xml`** — new section *Checkpoint ledger*. The state list stops at `QUEUE/DONE/ACTIVE/BRIEF`: status, no per-unit history. Add `states/<id>/` (`meta.txt`, `phase-<X>.{in-flight,done,failed}`, `history.log`) + three rules: (a) a marker write MUST fail loudly if `states/<id>/` does not exist — one creation path only (ghost-state-dir near-miss: a mistyped slug made a phantom dir; the dispatcher offered to redo a 4/7-done unit); (b) in-flight marker written *before* dispatch, so a crash is a stuck marker not silence; (c) `history.log` append-only, one line per transition (`<iso_ts> <phase> <in-flight|done|failed|rolled-back> <commit-or-reason>`).

**`02-phases.xml`** — Phase 1 gitignore gains `states/`; Phase 3a tick sweeps `phase-*.in-flight` older than N min with no live agent → dead-letter, not silent re-dispatch.

**`04-replenishment.xml`** — new section *Rollback is not retry* beside "Failed-batch retry" (today: re-queue + sonnet only — a wrong-but-consistent output has no path). `rollback <id> <phase>` = verify state dir → remove every marker at or after `<phase>` in lineage order → append `rolled-back` → requeue there. A missing marker MUST NOT read as "not started" without that record.

**Same file, Quota gate** — rationale gains: *prompt caching is hardcoded off for Agent-tool subagents (`anthropics/claude-code#29966`, filed 2026-03-02, open at last activity 2026-07-29; 54/54 dispatches zero cache reads, ~378k wasted tokens in one measured session; reproduced 2026-07-24). Treat every dispatch as full-price uncached input.* Fan-out consequences: the 50%-of-5h threshold is a floor, not a knob; prefer fewer larger batches, since a shared `BRIEF.md` prefix is re-paid per dispatch; file-reference dispatch becomes a cost rule, not hygiene.

**`05-anti-patterns.xml`** — new anti-pattern *Sizing fan-out as if the prefix were cached*.

**`poll-agents/AGENTS.md`** — fifth `success_criteria` ("every phase transition appends one line to `history.log`"), content-table row, 2.0.0 → 2.1.0, `last_verified: 2026-08-04`. `decisions.xml`: chose a file ledger over durable-execution frameworks and a SQL checkpointer.

**`idea-to-prod/content/40-cron-loop.xml`** — tick step 5 cannot distinguish "never dispatched" from "dispatched and died". Add: `state.md` records `dispatched=<task>` *before* dispatch; the one-line log IS the checkpoint.

**`idea-to-prod/content/50-failure-modes.xml`** — seventh mode *Output internally consistent but wrong*. Recovery: archive to `.product/rollback/<iso_ts>/`, revert `state.md` to phase N, append `rolled-back`, re-dispatch an amended brief. Three-strikes escalation routes here before the operator.

**`catalog.json`** — bump `version`/`last_verified`, extend `notes`, both workflows.

## New content proposed

**Slug:** `on-disk-checkpoint-ledger` · **Domain:** `ai-agents` · **Tier:** `solo`.
**Tier justification:** defect #6 — orchestration is 26/29 geek, nothing at solo or free. Bash, files and `flock`: no framework, no database, no Python. Our sharpest counter to "you need LangGraph".
**Produces:** a checkpoint-ledger spec for an existing queue/pool orchestrator — four fields (identity, snapshot, provenance, status), write boundaries (after each LLM call, after each non-idempotent side effect, before each likely-to-fail step, at each human gate), the identity guard, rollback-vs-retry — plus `templates/rollback.sh`, `templates/mark.sh`, `scripts/validate-on-disk-checkpoint-ledger.py`.
**Existing slugs checked:** `agent-replay-harness-cookbook`, `agent-rollback-button-design`, `record-replay-debugging`, `idempotent-write-tools`, `manual-override-ledger`, `mq-idempotent-consumers`, `auto-rollback-policy-design`, `experiment-ledger-discipline`, all seven `multi-agent-*`, `handoff-id-payload`, `subagent-as-context-firewall`, `stream-json-orchestration` — none covers run-level checkpointing.
**Registration:** (1) dir shaped after `ai-agents/context-graph-engineering/`; (2) `scripts/regen-tier-manifest.py`; (3) **hand-add** the `<methodology slug=… tier="solo">` block to `ai-agents/INDEX.xml` alphabetically, bump `count="103"` → `104` — never run `build-domain-index-v2.py`; (4) `validate-methodology-v2.py`, `-xml.py`, `-scripts.py`, `-templates.py`; (5) `CHANGELOG.md`; (6) back-refs from `agent-rollback-button-design`, `agent-replay-harness-cookbook`, `poll-agents/AGENTS.md`.

**Amendments** — no new slugs, no manifest change:

- `ai-agent-patterns` — dated block: all five frameworks Python/TS, no official Go path (Google ADK Go v2.1.0 GA 2026-07-23 excepted, and it still violates the caller/CLI split).
- `multi-agent-basics` — same + fracture note: AutoGen in maintenance since 2025-10, two incompatible successors (MS Agent Framework 1.0 GA 2026-04-03, .NET/Python; AG2 v1.0.1 2026-07-29).
- `multi-agent-conversational` — "AutoGen-style" is a pattern name, not a recommendation.
- `handoff-id-payload` + `multi-agent-orchestration-decision-tree` — input guardrails fire only on the first agent, output only on the last; validate per hop, never assume inheritance.
- `faion-cli-agent-adapter-pattern` — A2A row (`github.com/a2aproject/a2a-go`).

## CLI-orchestration boundary

Two places plus a citation: (1) authoritative — new ADR `faion-cli/.aidocs/decisions/ADR-cli-orchestration-artefact-boundary.md`, amending `constitution.md` line 27, with F023 (the binary already unpacks `scripts/` and `subagent-prompts/` to `~/.faion/`) as the precedent; (2) a pointer at line 27; (3) cited in `on-disk-checkpoint-ledger` as why the CLI never writes a checkpoint. **Not** in workflow content — workflows are caller-side.

> The CLI may emit and materialise deterministic orchestration artefacts — step manifests, scaffolded state directories, unpacked scripts and prompt files — but it MUST NOT spawn an LLM turn beyond the single search-ranking call it already makes, and it MUST NOT decide when to advance, retry, or roll back a step.

## Rejected

All six frameworks (Python/TS; no runtime Python ships). Embedding Google ADK Go — the rule is about *who orchestrates*, not language. A `faion orchestrate` subcommand. A SQL checkpointer (`flock` + files is correctly scaled). Automatic crash-resume — blind resume defeats the quota gate. A new framework-picker methodology — amend `ai-agent-patterns`. Separate slugs for CrewAI/AutoGen shapes.

## Risks / conflicts with other slices

- `ai-agents/INDEX.xml` — hand-edited; every slice adding an `ai-agents` slug touches it. Serialize: a conflict is silent index corruption the broken auto-builder cannot repair.
- `ADR-cli-orchestration-artefact-boundary.md` + `faion-cli/.aidocs/constitution.md` — Layer 2 slices (`spec-kit`, `kiro`, `openspec`, `constitution-md-pattern`) hit the same boundary. Author the ADR **once**; later slices amend.
- `llm-integration/prompt-cache-prefix-order` — Layer 4 may also claim #29966. Split: cost consequence in `04-replenishment.xml`, mechanics there, one cross-ref.
- `ai-agents/agent-replay-harness-cookbook` — names LangGraph; the `eval-harnesses` slice likely edits it too.
- `sdlc-ai/faion-cli-agent-adapter-pattern` — the Layer 1 MCP slice edits the same table for the 2026-07-28 break.
- `skills/faion/workflows/catalog.json` — bumped by any workflow-touching slice.
