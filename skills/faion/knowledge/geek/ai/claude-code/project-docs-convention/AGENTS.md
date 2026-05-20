---
slug: project-docs-convention
tier: geek
group: ai
domain: claude-code
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Convention for organizing documentation so both Claude Code and standalone agents (Agent SDK, subagents, autoheal) can discover and use the same context.
content_id: "412d623f6315d1e0"
tags: [documentation, claude-code, agents, convention, multi-agent]
---
# Project Documentation Convention

## Summary

**One-sentence:** Convention for organizing documentation so both Claude Code and standalone agents (Agent SDK, subagents, autoheal) can discover and use the same context.

**One-paragraph:** Convention for organizing documentation so both Claude Code and standalone agents (Agent SDK, subagents, autoheal) can discover and use the same context. Separates essential auto-loaded context (AGENTS.md) from detailed reference (in .agents/) using the @-ref pattern for Claude Code compatibility.

## Applies If (ALL must hold)

- Setting up a new repository or directory that will be worked on by both Claude Code and standalone agents (Agent SDK, autoheal, scheduled workers).
- Auditing an existing repository to ensure all directories have discoverable context for multi-agent pipelines.
- Onboarding a new project into the faion-network knowledge layer (CLAUDE.md + AGENTS.md pair required).
- Migrating a project from "all context in CLAUDE.md" to the two-file pattern for agent compatibility.

## Skip If (ANY kills it)

- Trivial directories with <3 files and no logic (e.g., empty `__init__.py` stubs) — skip creating the pair.
- External vendored code — do not add CLAUDE.md/AGENTS.md to third-party directories.
- Temporary scratch directories created during a build or test run — no documentation needed.

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

- parent skill: `geek/ai/claude-code/`
