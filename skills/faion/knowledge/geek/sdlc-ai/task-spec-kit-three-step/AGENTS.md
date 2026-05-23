---
slug: task-spec-kit-three-step
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces three versioned artifacts (spec.md, plan.md, tasks.md) in fixed order; only tasks.md is allowed to drive the coding agent.
content_id: "e0e174922d47a353"
complexity: medium
produces: spec
est_tokens: 5100
tags: [spec-kit, spec-driven-development, task-lifecycle, constitution-gate, artifact-order]
---
# Spec-Kit Three-Step Pipeline (specify → plan → tasks)

## Summary

**One-sentence:** Run the GitHub spec-kit chain /speckit.specify → /speckit.plan → /speckit.tasks so spec.md (WHAT/WHY) → plan.md (HOW) → tasks.md (parallelizable units) are produced in this fixed order before any code is written.

**One-paragraph:** Before any agent writes code, run the GitHub spec-kit chain `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` so the workflow yields three versioned artifacts in this fixed order: `spec.md` (WHAT/WHY with explicit `[NEEDS CLARIFICATION]` markers), `plan.md` (HOW + tech rationale + constitution gate evidence), and `tasks.md` (parallelizable work items, each tagged `[P]` if it can run concurrently). Only `tasks.md` is allowed to drive the coding agent — the spec, not the generated code, is the durable source of truth that survives model swaps and context resets.

**Ефективно для:**

- Greenfield feature, де модель часом скаче через 2-3 sessions.
- Constitution-driven repos: plan.md цитує rules, code їх не порушує.
- Parallel agent fleets: [P]-tagged tasks бігають одночасно без conflicts.
- Audit для compliance: spec/plan/tasks — три versioned артефакти, легко переглянути.

## Applies If (ALL must hold)

- Greenfield feature or non-trivial enhancement (not a single-file bugfix).
- Team plans to drive coding agents across multiple sessions or model versions.
- Constitution / architecture standards exist and the plan must cite them.

## Skip If (ANY kills it)

- Bug fix where the spec is the failing test.
- Throwaway prototype not destined for production.
- No constitution / architecture standards exist yet — write those first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature request | Markdown / ticket | PM |
| Constitution / standards | Markdown | repo `/docs/constitution.md` |
| spec-kit CLI installed | binary | developer machine |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-skeleton.md` | spec.md skeleton with [NEEDS CLARIFICATION] markers and WHAT/WHY sections. |
| `templates/tasks-skeleton.md` | tasks.md skeleton with [P] tag column and file-overlap proof column. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-task-spec-kit-three-step.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[task-plan-mode-locked-execution]]
- [[task-worktree-runtime-isolation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
