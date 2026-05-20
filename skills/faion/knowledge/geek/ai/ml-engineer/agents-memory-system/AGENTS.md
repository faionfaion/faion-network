---
slug: agents-memory-system
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Autonomous agents running long tasks overflow their context window without explicit memory management.
content_id: "e294125be6147459"
tags: [agents, memory, vector-store, context-management, embeddings]
---
# Agent Memory System — Short-Term, Long-Term, and Context Management

## Summary

**One-sentence:** Autonomous agents running long tasks overflow their context window without explicit memory management.

**One-paragraph:** Autonomous agents running long tasks overflow their context window without explicit memory management. A three-tier memory architecture — short-term conversation buffer, long-term vector store, episodic task log — keeps agents grounded across sessions. Summarize conversation history every N steps; use cosine similarity recall to inject only relevant past experiences rather than raw history.

## Applies If (ALL must hold)

- Long-running agents that execute more than 20 steps in a single session.
- Agents that handle recurring similar tasks and should learn from past runs.
- Agents that must remember user preferences or domain knowledge across sessions.
- Multi-session research or content generation workflows where context exceeds 50K tokens.

## Skip If (ANY kills it)

- Single-turn agents completing in under 10 steps — memory overhead exceeds value.
- Tasks where all necessary context fits in one context window — adding memory layers introduces complexity with no benefit.
- Strict reproducibility requirements — memory recall is non-deterministic, which conflicts with auditing needs.

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

- parent skill: `geek/ai/ml-engineer/`
