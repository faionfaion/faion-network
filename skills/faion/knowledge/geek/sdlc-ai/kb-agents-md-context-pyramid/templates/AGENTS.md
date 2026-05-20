---
slug: templates
tier: geek
group: sdlc-ai
domain: kb-agents-md-context-pyramid
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reusable templates for implementing the three-tier context pyramid: CLAUDE.
content_id: "180a580e913ae900"
tags: [documentation, agents-md, context-pyramid, claude-code, templates]
---
# AGENTS.md Context Pyramid Templates

## Summary

**One-sentence:** Reusable templates for implementing the three-tier context pyramid: CLAUDE.

**One-paragraph:** Reusable templates for implementing the three-tier context pyramid: CLAUDE.md is a one-line hook that references AGENTS.md, AGENTS.md is a 20-80 line essential brief auto-loaded by both Claude Code and standalone agents, and .agents/INDEX.md is the on-demand catalogue of deep references. The convention enforces one source of truth and per-directory agent context calibration.

## Applies If (ALL must hold)

- Any repo where multiple agent kinds (Claude Code + Codex + aider + custom Agent SDK) need to share project context.
- Multi-package monorepos where each subpackage has different commands, gotchas, and dependencies.
- Long-lived projects where decision history and architecture deep-dives must stay searchable but not auto-loaded.
- Migrating from a single bloated CLAUDE.md to a routing-friendly layout.

## Skip If (ANY kills it)

- Single-file scripts or one-off notebooks — the convention's overhead exceeds the benefit.
- Generated directories (build output, vendored deps) — they get rewritten and the docs would drift.
- Trivial leaf folders with under three files and no agent-relevant logic — keep the parent's AGENTS.md instead.

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

- parent skill: `geek/sdlc-ai/kb-agents-md-context-pyramid/`
