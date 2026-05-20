---
slug: ai-agent-patterns
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Six structured patterns for building agentic AI systems: ReAct (Thought-Action-Observation loop), Chain-of-Thought, Tool Use, Plan-Execute, Reflection, and Tree-of-Thoughts — plus multi-agent coordination topologies (Sequential, Parallel, Supervisor, Hierarchical).
content_id: "ae3d45909ea9b747"
tags: [agents, patterns, agentic-ai, architecture, llm]
---
# AI Agent Design Patterns

## Summary

**One-sentence:** Six structured patterns for building agentic AI systems: ReAct (Thought-Action-Observation loop), Chain-of-Thought, Tool Use, Plan-Execute, Reflection, and Tree-of-Thoughts — plus multi-agent coordination topologies (Sequential, Parallel, Supervisor, Hierarchical).

**One-paragraph:** Six structured patterns for building agentic AI systems: ReAct (Thought-Action-Observation loop), Chain-of-Thought, Tool Use, Plan-Execute, Reflection, and Tree-of-Thoughts — plus multi-agent coordination topologies (Sequential, Parallel, Supervisor, Hierarchical). Choosing the right pattern at design time is more important than implementation details.

## Applies If (ALL must hold)

- Selecting an architecture before building any agentic system
- Replacing informal LLM loops with debuggable, observable patterns
- Multi-step workflows where intermediate results determine next steps (ReAct, Plan-Execute)
- Quality-critical outputs where first-pass is insufficient (Reflection)
- Multi-agent coordination with specialized workers

## Skip If (ANY kills it)

- Single LLM call with deterministic output — patterns add latency and cost without benefit
- Full input fits in one context window with no tool calls — just prompt directly
- Real-time inference under 200ms — ReAct, Reflection, and ToT require multiple round-trips
- Reproducible outputs for strict auditing — agent non-determinism conflicts with reproducibility requirements

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
