---
slug: llm-friendly-architecture
tier: geek
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Architecture patterns that keep individual source files between 100-300 lines, use flat directory structures (max 3 levels), self-documenting file names, and explicit imports — designed to reduce LLM edit errors caused by large files and hidden import chains.
content_id: "48b2ce2c73875da4"
tags: [llm, architecture, file-size, code-quality, typescript, react]
---
# LLM-Friendly Architecture

## Summary

**One-sentence:** Architecture patterns that keep individual source files between 100-300 lines, use flat directory structures (max 3 levels), self-documenting file names, and explicit imports — designed to reduce LLM edit errors caused by large files and hidden import chains.

**One-paragraph:** Architecture patterns that keep individual source files between 100-300 lines, use flat directory structures (max 3 levels), self-documenting file names, and explicit imports — designed to reduce LLM edit errors caused by large files and hidden import chains.

## Applies If (ALL must hold)

- Designing the initial structure of a new TypeScript/React/Python project that will use Claude Code for feature development.
- During code review: flagging god components, barrel re-exports, or files exceeding 300 lines before they merge.
- When an agent repeatedly makes wrong edits on a specific file — the root cause is almost always file size or ambiguous naming.
- Migrating a legacy codebase to LLM-friendly patterns in preparation for AI-assisted feature development.

## Skip If (ANY kills it)

- Auto-generated files (GraphQL schemas, protobuf, ORM migrations, locale bundles) — size limits do not apply.
- Highly stable, rarely-changed modules where the refactoring cost exceeds the benefit.
- Performance-sensitive Python CLI startup: many small files increase import time; profile before splitting.
- Projects without any AI-assisted development planned — the patterns add value but are not mandatory for human-only teams.

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

- parent skill: `geek/dev/software-developer/`
