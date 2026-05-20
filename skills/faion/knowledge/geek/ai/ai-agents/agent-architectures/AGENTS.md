---
slug: agent-architectures
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-ready architectures for autonomous agents with memory, tools, and planning capabilities.
content_id: "a8a3f8d625a6295f"
tags: [agents, architecture, production, memory, tools]
---
# Agent Architectures

## Summary

**One-sentence:** Production-ready architectures for autonomous agents with memory, tools, and planning capabilities.

**One-paragraph:** Production-ready architectures for autonomous agents with memory, tools, and planning capabilities.

## Applies If (ALL must hold)

- Building a production autonomous agent that requires persistent memory, tool use, and failure recovery
- Designing the state machine for a multi-step agent workflow (IDLE → PLANNING → EXECUTING → REFLECTING → COMPLETE)
- Implementing a memory system (short-term + long-term with embedding-based retrieval) for a Claude subagent
- Replacing a monolithic prompt chain with a proper tool-equipped agent that can handle partial failures

## Skip If (ANY kills it)

- Simple single-step LLM tasks where the architecture overhead is not justified
- When the task graph is fully deterministic (no conditional branching based on tool results); use a chain instead of an agent
- Latency-critical paths where multi-iteration ReAct loops add unacceptable delay
- When you don't control the execution environment (e.g., no way to sandbox tool calls or enforce iteration limits)

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

- parent skill: `geek/ai/ai-agents/`
