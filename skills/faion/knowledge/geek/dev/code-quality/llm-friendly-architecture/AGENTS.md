---
slug: llm-friendly-architecture
tier: geek
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Architecture patterns that keep individual source files between 100-300 lines, use flat directory structures (max 3 levels), self-documenting file names, and explicit imports — designed to reduce LLM edit errors caused by large files and hidden import chains.
content_id: "48b2ce2c73875da4"
tags: [llm, architecture, file-size, code-quality, ai-assisted]
---
# LLM-Friendly Architecture

## Summary

**One-sentence:** Architecture patterns that keep individual source files between 100-300 lines, use flat directory structures (max 3 levels), self-documenting file names, and explicit imports — designed to reduce LLM edit errors caused by large files and hidden import chains.

**One-paragraph:** Architecture patterns that keep individual source files between 100-300 lines, use flat directory structures (max 3 levels), self-documenting file names, and explicit imports — designed to reduce LLM edit errors caused by large files and hidden import chains.

## Applies If (ALL must hold)

- Planning a new codebase where Claude Code or similar AI tools will handle ongoing development.
- Refactoring an existing repo where AI-assisted edits frequently produce wrong line numbers or missed imports.
- Code review: auditing PRs where files exceed 300 lines before merging.
- After a retrospective identifies "AI tool makes mistakes in large files" as a recurring problem.

## Skip If (ANY kills it)

- Generated code (protobuf outputs, ORM migrations, auto-generated clients) — file size limits don't apply to machine-generated files.
- Legacy monolith stabilization where any structural change risks regressions; defer architecture until test coverage is in place.
- Performance-critical CLI hot paths where splitting files increases import overhead.
- Teams not using AI tooling — enforced decomposition overhead may outweigh benefit.

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

- parent skill: `geek/dev/code-quality/`
