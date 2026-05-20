---
slug: agent-patterns
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implementation patterns for different types of autonomous agents.
content_id: "e453c96adfeaa261"
tags: [agents, patterns, react, planning, reflexion]
---
# Agent Patterns

## Summary

**One-sentence:** Implementation patterns for different types of autonomous agents.

**One-paragraph:** Implementation patterns for different types of autonomous agents. ReAct is general-purpose task execution with reasoning and tool calls. Plan-and-Execute creates a plan upfront then executes steps sequentially. Reflexion uses self-critique and retry for tasks requiring iteration and self-correction.

## Applies If (ALL must hold)

- Complex multi-step tasks requiring tool orchestration
- Research and analysis workflows where the agent may need to recover from dead ends
- Code generation and execution workflows
- When tasks require iteration and self-correction
- Automating knowledge work that would normally require human iteration

## Skip If (ANY kills it)

- Single-step lookup or retrieval where overhead is wasteful
- Latency-sensitive paths where one round-trip must complete in under 2 seconds
- Tasks with no verifiable success criterion (Reflexion loop has no termination signal)
- Environments without tool access where ReAct degenerates to plain chain-of-thought
- Budget-constrained situations where multiple LLM calls are prohibitive

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
