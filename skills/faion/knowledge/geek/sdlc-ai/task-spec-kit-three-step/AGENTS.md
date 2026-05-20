---
slug: task-spec-kit-three-step
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Before any agent writes code, run the GitHub spec-kit chain `/speckit.
content_id: "7fb80600d9b688e3"
tags: [spec-kit, spec-driven-development, task-lifecycle, constitution-gate, artifact-order]
---
# Spec-Kit Three-Step Pipeline (specify → plan → tasks)

## Summary

**One-sentence:** Before any agent writes code, run the GitHub spec-kit chain `/speckit.

**One-paragraph:** Before any agent writes code, run the GitHub spec-kit chain `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` so the workflow yields three versioned artifacts in this fixed order: `spec.md` (WHAT/WHY with explicit `[NEEDS CLARIFICATION]` markers), `plan.md` (HOW + tech rationale + constitution gate evidence), and `tasks.md` (parallelizable work items, each tagged `[P]` if it can run concurrently). Only `tasks.md` is allowed to drive the coding agent — the spec, not the generated code, is the durable source of truth that survives model swaps and context resets.

## Applies If (ALL must hold)

- Any non-trivial feature touching more than ~3 files or one service boundary.
- High-stakes domains traceable to a regulator or contract: payments, auth, migrations, PII flows.
- Multi-agent fan-out where each parallel agent needs an isolable task with its own AC.
- Greenfield modules where the public API surface is the artifact others will depend on.

## Skip If (ANY kills it)

- True one-line bug fixes, typo corrections, dependency patch bumps — spec ceremony exceeds the change.
- Throwaway exploratory spike branches whose code is committed but never merged.
- `npm audit fix` / `cargo update` style mechanical work — Renovate/Dependabot, not spec-kit.
- Pure ops tasks with no code change (cert renewal, DNS edit) — runbook, not spec.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
