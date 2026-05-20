---
slug: pattern-memory
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A system for capturing, storing, and retrieving proven solutions from development sessions so LLM agents apply consistent patterns across tasks and projects.
content_id: "83e040d73d37548d"
tags: [pattern-memory, learning, reflexion, agent-memory, knowledge-capture]
---
# Pattern Memory

## Summary

**One-sentence:** A system for capturing, storing, and retrieving proven solutions from development sessions so LLM agents apply consistent patterns across tasks and projects.

**One-paragraph:** A system for capturing, storing, and retrieving proven solutions from development sessions so LLM agents apply consistent patterns across tasks and projects. Patterns are stored in `.aidocs/memory/patterns.md` with a confidence score (0.5 initial → 0.9+ proven), graduated by number of successful uses. High-confidence patterns (0.8+) are synced to `CLAUDE.md` for immediate availability in new sessions. The rule: capture when a non-obvious solution works in 2+ distinct contexts; never capture obvious best practices or one-off fixes.

## Applies If (ALL must hold)

- After a successful task execution where a non-obvious solution was applied — capture before the session ends
- When the same problem appears for the second time in a different context — that is a pattern, not a one-off
- Before starting a new task wave — inject high-confidence patterns (0.8+) into the task context header
- During CLAUDE.md maintenance: sync established patterns (0.9+) into the project rules file
- When onboarding a new agent session that lacks project history — load `patterns.md` as working memory

## Skip If (ANY kills it)

- Capturing well-known best practices already in framework docs (e.g., "use async/await")
- One-off fixes specific to a single file or edge case
- Patterns with confidence below 0.5 (only one use, unverified) — capture as candidate, do not promote
- Project-specific configuration values (API keys, URLs) — those go in `.env`, not patterns

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

- parent skill: `solo/sdd/sdd/`
