# Writing Design Documents

## Summary

A design document answers HOW to build a feature. It bridges spec (WHAT) and code (RESULT) by recording architectural decisions (AD-X), file structure, data models, and API contracts before any implementation begins. Required when a feature touches 5+ files, changes a DB schema, modifies an API contract, or introduces cross-service dependencies. Every FR-X from the spec must trace to at least one AD-X. Every AD-X must include alternatives considered — a decision with only one option is not a real decision.

## Why

Writing forces clarity that diagrams and code cannot. Unstructured text is the better tool for solving problems early — changes are cheap on paper, expensive in code (Google Engineering). Design docs give LLM execution agents explicit file structure, type definitions, and API contracts; without these, parallel agents produce incompatible implementations. AD-X decisions marked `Proposed` must not be implemented — the agent must wait for human approval before executing.

## When To Use

- After spec.md is approved and before writing implementation-plan.md
- Feature touches 5+ files, changes a DB schema, modifies an API contract, or has cross-service dependencies
- When the team needs an explicit record of alternatives considered to prevent re-litigating decisions
- When onboarding a new agent into an existing codebase — design.md gives full architectural context

## When NOT To Use

- Bug fixes touching 1-2 files with no architectural impact
- Small refactors with no interface changes
- Features whose entire scope fits in a single task under ~5k tokens
- Greenfield experiments or spikes where the design is deliberately exploratory

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Document hierarchy (constitution → spec → design → impl-plan); SDD-optimized structure; AD-X decision format; Y-statement |
| `content/02-for-llm.xml` | LLM code generation patterns: explicit file patterns, type definitions, API contracts, reference tables; doc types comparison (RFC/TDD/ADR/mini) |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-sdd.md` | Full SDD design.md template: AD-X, file structure, data models, API contracts, traceability |
| `templates/design-rfc.md` | RFC (Request for Comments) template based on HashiCorp format |
| `templates/design-tdd.md` | Technical Design Document template with 12 numbered sections |
| `templates/design-adr.md` | Architecture Decision Record (ADR) template, Michael Nygard format |
| `templates/design-mini.md` | Lightweight 1-page design template for small changes |
| `templates/prompt-design.txt` | Prompts for drafting design.md and reviewing for traceability and completeness |
| `templates/validate-design.sh` | Shell script checking that every AD-X block has Status, Decision, and Rationale fields |
