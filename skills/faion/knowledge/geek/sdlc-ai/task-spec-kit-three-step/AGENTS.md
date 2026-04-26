# Spec-Kit Three-Step Pipeline (specify → plan → tasks)

## Summary

Before any agent writes code, run the GitHub spec-kit chain `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` so the workflow yields three versioned artifacts in this fixed order: `spec.md` (WHAT/WHY with explicit `[NEEDS CLARIFICATION]` markers), `plan.md` (HOW + tech rationale + constitution gate evidence), and `tasks.md` (parallelizable work items, each tagged `[P]` if it can run concurrently). Only `tasks.md` is allowed to drive the coding agent — the spec, not the generated code, is the durable source of truth that survives model swaps and context resets.

## Why

Free-form chat with an LLM produces code that drifts from intent within 2-3 turns; nothing in the conversation is versioned, the acceptance criteria are unrecoverable, and `[NEEDS CLARIFICATION]` markers never surface so the model silently guesses. Spec-kit injects a constitution of nine immutable principles (library-first, test-first, simplicity gate, anti-abstraction, integration-first testing, etc.) as automated template gates, so the LLM is constrained toward higher-quality output and the spec acts as a deterministic anchor across context swaps. GitHub published the toolkit open-source in Sept 2025; by April 2026 it is the reference implementation of Spec-Driven Development across Claude Code, Codex, Cursor, and Gemini CLI.

## When To Use

- Any non-trivial feature touching more than ~3 files or one service boundary.
- High-stakes domains traceable to a regulator or contract: payments, auth, migrations, PII flows.
- Multi-agent fan-out where each parallel agent needs an isolable task with its own AC.
- Greenfield modules where the public API surface is the artifact others will depend on.

## When NOT To Use

- True one-line bug fixes, typo corrections, dependency patch bumps — spec ceremony exceeds the change.
- Throwaway exploratory spike branches whose code is committed but never merged.
- `npm audit fix` / `cargo update` style mechanical work — Renovate/Dependabot, not spec-kit.
- Pure ops tasks with no code change (cert renewal, DNS edit) — runbook, not spec.

## Content

| File | What's inside |
|------|---------------|
| `content/01-three-artifact-order.xml` | The fixed `spec.md` → `plan.md` → `tasks.md` order, the prohibition on coding before `tasks.md`, and the role of `[NEEDS CLARIFICATION]`. |
| `content/02-constitution-gate.xml` | How the spec-kit constitution acts as automated gate inside `plan.md`; the nine principles and the agent's obligation to record gate evidence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-skeleton.md` | Minimal `spec.md` skeleton with required sections and `[NEEDS CLARIFICATION]` markers. |
| `templates/tasks-skeleton.md` | `tasks.md` skeleton with `[P]` parallel-marker convention and `Closes #N` anchor field. |
