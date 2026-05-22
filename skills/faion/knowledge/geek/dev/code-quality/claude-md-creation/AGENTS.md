---
slug: claude-md-creation
tier: geek
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: CLAUDE.
content_id: "87691b316f76ba53"
tags: [claude-code, documentation, conventions, project-setup, ai-integration]
---
# CLAUDE.md Creation

## Summary

**One-sentence:** CLAUDE.

**One-paragraph:** CLAUDE.md is a project-specific instruction file that provides Claude Code with context about the codebase, conventions, and workflows. A well-crafted CLAUDE.md enables Claude to work more effectively within your project's constraints, covering tech stack, quick commands, project structure, code conventions, and git workflow.

## Applies If (ALL must hold)

- Bootstrapping a new repo for Claude Code: no CLAUDE.md exists and the codebase has project-specific conventions.
- Onboarding a pre-existing codebase: commands, structure, and lint rules need to be machine-readable in context.
- After significant project restructuring: existing CLAUDE.md is stale (wrong commands, removed paths).
- In multi-agent setups where multiple subagents share the same repo and need a consistent orientation doc.

## Skip If (ANY kills it)

- Single-file scripts or throwaway prototypes with no conventions worth capturing.
- Projects where CLAUDE.md already exists and is accurate — updating one section is not a full creation task.
- Documentation-only repos with no commands to run and no code conventions to enforce.

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
