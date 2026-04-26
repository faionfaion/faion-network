# Design Document Structure

## Summary

A design document answers "HOW are we building this?" — it bridges spec (what) and code (impl).
The canonical structure is: reference docs, overview, FR/AD traceability matrix, architectural
decisions (AD-X) with alternatives and consequences, file change table (CREATE/MODIFY), data
models, API contracts, security, performance, testing strategy, and migration plan. Every file
change must trace to an FR and an AD.

## Why

Without a design document, executor agents make local decisions that break overall architecture,
generate files not required by any FR, and produce API contracts that drift from spec ACs.
The FR → AD traceability matrix is the quality gate: if every FR has an AD, and every file
change traces to both, the implementation is complete by construction. Human reviewers
need only check the AD alternatives and consequences sections — the rest is verifiable.

## When To Use

- After `spec.md` is approved and before writing the implementation plan
- Feature has non-trivial architectural decisions: schema, API contracts, auth, caching
- Code will be written by an agent executor — design.md is the authoritative file-creation instruction
- Feature spans multiple files or services requiring explicit data flow definition
- Security or performance concern exists — these sections create explicit review targets

## When NOT To Use

- Single-file, single-concern changes with no architectural decisions (waste)
- `spec.md` is still Draft — design decisions cannot be made until requirements are stable
- Internal refactors with no API/schema changes — write an ADR instead
- Spike/research tasks: output is an ADR or updated spec, not a design doc

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Full design.md section list, comparison to spec/impl-plan, document hierarchy |
| `content/02-checklist.xml` | Phase-by-phase authoring checklist: prerequisites, overview, AD-X, file table, data models, testing, quality gate |
| `content/03-gotchas.xml` | Antipatterns and AI-agent failure modes specific to design documents |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-template.md` | Canonical design.md template v2.0 with all sections and placeholder text |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/design-quality-gate.sh` | Verify every spec FR appears in design; check file table traces to FR and AD |
