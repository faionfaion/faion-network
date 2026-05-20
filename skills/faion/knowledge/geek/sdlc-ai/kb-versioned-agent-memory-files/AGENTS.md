---
slug: kb-versioned-agent-memory-files
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Persist long-term agent memory as four committed Markdown files in.
content_id: "a00e474f3e9c25b4"
tags: [agent-memory, versioned-memory, decisions, patterns, session-state]
---
# Versioned Agent-Memory Files (decisions / patterns / mistakes)

## Summary

**One-sentence:** Persist long-term agent memory as four committed Markdown files in.

**One-paragraph:** Persist long-term agent memory as four committed Markdown files in .aidocs/memory/ (or .product/memory/): decisions.md (key technical choices), patterns.md (proven implementations), mistakes.md (errors and the fix), and session.md (in-flight state). Every entry is appended (never edited or auto-overwritten by an LLM), every entry carries a date and a citation back to the commit, ticket, or transcript that produced it. Agents read the four files at session start; session.md is the only file that resets between sessions. The convention turns "agent memory" from a vendor-specific RAG black box into a reviewable, diff-able, code-reviewed artifact.

## Applies If (ALL must hold)

- Long-lived projects (>3 months) where agent context resets every session and rebuilds from scratch.
- Multi-agent setups (Claude Code + Codex + autoheal cron) that must share institutional knowledge.
- Teams where a human reviewer should approve every change to "what the agent believes about this codebase".
- Replacing vendor-specific memory features whose contents you cannot inspect or version.

## Skip If (ANY kills it)

- One-shot agent invocations or short-lived feature branches — the four-file overhead is wasted.
- Highly volatile prototypes where today's "decision" is tomorrow's discard.
- Non-deterministic transient state (queue depths, in-flight ticket IDs) — those belong in a runtime store, not in versioned memory.

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
