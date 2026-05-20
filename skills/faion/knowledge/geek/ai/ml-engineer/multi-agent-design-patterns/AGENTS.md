---
slug: multi-agent-design-patterns
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Four canonical patterns for orchestrating multiple AI agents: Supervisor, Hierarchical, Sequential, and Peer-to-Peer.
content_id: "327445e5c4bf55f6"
tags: [agents, orchestration, design-patterns, multi-agent, langgraph]
---
# Multi-Agent Design Patterns

## Summary

**One-sentence:** Four canonical patterns for orchestrating multiple AI agents: Supervisor, Hierarchical, Sequential, and Peer-to-Peer.

**One-paragraph:** Four canonical patterns for orchestrating multiple AI agents: Supervisor, Hierarchical, Sequential, and Peer-to-Peer. Choose the simplest pattern; includes design checklists and production-readiness gates.

## Applies If (ALL must hold)

- Single agent context window is insufficient for the full task
- Tasks have parallelizable subtasks (research + writing + validation can run concurrently)
- Domain expertise must be isolated — a billing agent must not have access to CRM tools
- Enterprise workflows map naturally to organizational units (teams, departments, roles)
- Reliability requires cross-checking: parallel agents can validate each other's outputs

## Skip If (ANY kills it)

- Simple single-step tasks — multi-agent adds coordination overhead with no benefit
- Latency is critical (<2s) — agent-to-agent round trips add 500ms–2s each
- The problem is not well-decomposed yet — build a working single agent first, then extract workers
- Token budget is constrained — multi-agent systems use significantly more tokens per task
- Infrastructure cannot reliably run concurrent agent processes

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
