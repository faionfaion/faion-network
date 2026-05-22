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
tags: [claude-code, documentation, project-setup, ai-assisted-dev]
---
# CLAUDE.md Creation

## Summary

**One-sentence:** CLAUDE.

**One-paragraph:** CLAUDE.md is a project-specific instruction file that gives Claude Code the context it needs: commands, structure, conventions, and gotchas. A well-crafted CLAUDE.md (under 150 lines) eliminates the back-and-forth of Claude asking basic questions about the project setup.

## Applies If (ALL must hold)

- Starting a new project where Claude Code will be the primary AI assistant.
- Inheriting a codebase and needing to orient Claude to existing conventions before making changes.
- After a major dependency upgrade or framework migration that invalidates existing instructions.
- Setting up per-module CLAUDE.md files in a monorepo where modules have different stacks.

## Skip If (ANY kills it)

- Throwaway scripts or single-file utilities with no ongoing AI-assisted development.
- Projects where team policy prohibits AI coding tools entirely.
- When an accurate CLAUDE.md already exists — update specific sections rather than recreating.

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
