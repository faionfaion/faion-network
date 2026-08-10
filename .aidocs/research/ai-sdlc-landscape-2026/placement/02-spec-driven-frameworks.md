# Placement — Spec-Driven Frameworks
**Slice:** Spec Kit, Kiro, OpenSpec, Agent OS, Tessl · **Author pass:** 2 of 10 · **Date:** 2026-08-04

## Verdict summary

| Approach | Verdict | Placement | Target path |
|---|---|---|---|
| Spec Kit | 🟡 | new methodology + stale-slug update + workflow-edit | `sdd/spec-drift-convergence-loop/`; `sdlc-ai/task-spec-kit-three-step/` v2.0.0; `sdd-batch-orchestrator/content/07-*.xml` |
| Kiro | 🟡 | workflow-edit (entry gate + artefact alias) | `sdd-batch-orchestrator/content/{02-phases,05-defaults-constraints}.xml`; `idea-to-prod/content/20-phases.xml` |
| OpenSpec | 🟡 | comparison object; mechanics go to the sibling spec-delta pass | `sdd/spec-driven-framework-selection/` |
| Agent OS | 🟡 | workflow-edit; no new slug | `sdd-batch-orchestrator/content/02-phases.xml` (PLAN) |
| Tessl | 🔴 | decision aid — "why not spec-as-source" | `spec-driven-framework-selection/content/04-rungs-and-the-tessl-case.xml` |

## Workflow changes

**1. `sdd-batch-orchestrator/content/07-verify-review-fix-loop.xml`** — new `<section title="Convergence re-derivation">` after `Termination`. Once REVIEW returns PASS, one append-only pass reads `spec.md` + `plan.md ## Execution Plan` + `constitution.md` as sole intent, assesses the **present state of the code** (not a `git diff`), and emits unbuilt work as **new `TASK_*.md`**. It MUST NOT edit `spec.md`, `plan.md`, task numbering or code; writes nothing when clean; MUST NOT run before EXECUTE. Replaces nothing — today the loop ends at PASS. Source: Spec Kit `converge.md`, v0.11.2 (2026-06-18).

**2. `sdd-batch-orchestrator/decisions.xml`** — append `topic="converge-inside-review-loop"` (2026-08-04): chose a step inside the bounded loop; rejected a 13th phase (breaks the locked 12-phase decision of 2026-05-02) and an LLM-judge verdict (non-deterministic gate — the Tessl lesson).

**3. `sdd-batch-orchestrator/content/05-defaults-constraints.xml`** — under *Required positives*, an **entry gate**: EXECUTE MUST NOT dispatch for a feature whose `spec.md` still carries unresolved clarification markers. Our gates are exit-only (`readiness.md` before `done/`); Kiro's blockable `PreTaskExec` is where an entry gate belongs.

**4. `sdd-batch-orchestrator/content/02-phases.xml`** — Phase 3 PLAN gains one instruction: identify reference implementations already in the codebase before writing `## Design` (Agent OS `shape-spec`). Add the alias line `requirements.md → spec.md`, `design.md → plan.md ## Design`, `tasks.md → ## Execution Plan` + `TASK_*.md`.

**5. `idea-to-prod/content/20-phases.xml`** — **stale**. Phase 3 still writes the "SDD quartet: `spec.md`, `design.md`, `test-plan.md`, `implementation-plan.md`". Replace with `spec.md` (delta-only when `project-spec/` exists), `plan.md`, conditional `user-flows.md` / `ui-ux-design.md`, `TASK_*.md`, `readiness.md`. Phase 6: swap `per test-plan.md` for `per user-flows.md`, gate on `readiness.md`.

**6. `workflows/catalog.json`** — bump `sdd-batch-orchestrator` → `2.1.0`, `idea-to-prod` → `1.1.0`, `last_verified: 2026-08-04`; that plus a CHANGELOG entry is the whole registration.

## New content proposed

Registration, A and B: folder shaped like `ai-agents/context-graph-engineering/` (`AGENTS.md` without frontmatter + `meta.json` + `content/NN-*.xml`) → `regen-tier-manifest.py` → hand-add `<methodology slug=… tier=… path=…>` to `sdd/INDEX.xml`, bump `count`. Never run `build-domain-index-v2.py`.

**A. `spec-driven-framework-selection`** · `sdd` · **solo** — "which of these five do I use" is the buyer's entry question, and the one place our `project-spec/` advantage is demonstrable rather than asserted. Produces a decision record: per framework, dated state + cost + enforced-vs-prose; the artefact alias table; Böckeler's spec-first / spec-anchored / **spec-as-source** ladder with us pinned at spec-anchored and Tessl the worked failure of the top rung. Checked, none cover it: `sdd-workflow-overview` (our phases only), `best-practices-2026` (stack rubric), `key-trends-summary` (trends, no tools), `quality-gates`, `spec-requirements`, `project-spec-structure`, `task-spec-kit-three-step` (one tool, no comparison).

**B. `spec-drift-convergence-loop`** · `sdd` · **pro** — the tool-independent `converge`: intent + constitution in, present-state assessment, append-only output, unchanged when clean, refuses to run pre-implementation. Checked: `quality-gates-confidence` and `quality-gates` gate before done, `readiness-checklist` gates the move to `done/`; none re-derive remaining work. Ships a deterministic `scripts/validate-spec-drift-convergence-loop.py`.

**C. `sdlc-ai/task-spec-kit-three-step`** — **update, not new**: v`2.0.0`, `last_reviewed: 2026-08-04`. It teaches a three-step pipeline; Spec Kit has ten commands and `converge` post-dates its review. Rescope to "the three artefact layers, tool-independent" and drop the version-pinned chain — v0.11 → v0.15.2 in five weeks means any command sequence rots. `meta.json` edit → `regen-tier-manifest.py`; its `INDEX.xml` entry exists, update the summary in place.

## F049 disposition

**Do not ship as a CLI feature.** Move `.aidocs/in-progress/feature-049-spec-deltas-bdd-cli/` → `.aidocs/backlog/`. Grounds: (a) its `.aidocs/specs/<capability>/` tree forks the source of truth away from the richer `project-spec/` — the drift `project-spec/` exists to solve; (b) `faion sdd diff` rebuilds a verb OpenSpec **removed in v0.2.0**, redirecting to `show`; (c) it validates `test-plan.md`, gone from the lifecycle; (d) ROI is gone — our specs are already 64% delta, ~150–250 tokens/feature; (e) `faion-cli` is a Go binary, so `faion_cli/sdd/` has no home. Surviving as content, not a command: RENAMED as a fourth verb, merge order RENAMED → REMOVED → MODIFIED → ADDED, scenario-loss detection, ERROR/WARNING/INFO — the sibling spec-delta pass's.

## Rejected

`.specify/` as a fourth agent-owned root. The 10-command chain and the `plan.md` + `tasks.md` split (re-inflates what we merged). `[P]` tags, `taskstoissues`, steering-file sprawl, ALL-CAPS EARS. Kiro Quick Spec — gate-free generation is the failure SDD prevents. Any `uv`/`npx`/Node install in customer-facing content. Tessl's registry as a distribution channel. Agent OS `standards-extraction-from-codebase` as a new slug — `dark-knowledge-extraction-protocol` and `client-style-guide-importer` (both pro) already cover tacit extraction and imported conventions; at most a scope extension, and that call needs both read first. Agent OS's full-text-vs-reference rule is **already ours** (`file-reference-dispatch`, `on-disk-file-layout-as-contract`).

## Risks / conflicts with other slices

- `sdd/INDEX.xml` — every sdd-adding pass edits it plus `count="90"`. Append by hand; never regenerate. Aside: 8 on-disk dirs are still absent from it — the seven lifecycle methodologies (`cr-bug-tracking`, `plan-md-structure`, `project-spec-structure`, `quality-gates`, `readiness-checklist`, `ui-ux-design-template`, `user-flows-template`) plus `templates` — though all seven now appear in `tier-manifest.json`. The manifest half of corpus defect #1 is fixed; the index half is not.
- `skills/tier-manifest.json` — regenerate once after all ten passes, not per pass. `workflows/catalog.json` — any workflow-editing pass bumps a version; serialize.
- `sdd-batch-orchestrator/content/07-verify-review-fix-loop.xml` + `decisions.xml` — the reliability pass (verification ladder, llm-as-judge) targets the same loop; merge, do not overwrite.
- `idea-to-prod/content/20-phases.xml` — the orchestration pass (checkpoint/rollback) touches the same phase list; my edit is confined to Phase 3's artefact set and Phase 6's `test-plan.md` line. An sdlc-ai pass may also claim `task-spec-kit-three-step/`.
- Pass 1 owns EARS, `constitution.md` and spec-delta as *patterns*; A cross-references their slugs, never restating grammar, amendment procedure or merge order.
- Unowned: `sdd/sdd-workflow-overview` still describes a five-phase `spec → design → impl-plan → tasks → review` lifecycle that no longer matches our documents.
