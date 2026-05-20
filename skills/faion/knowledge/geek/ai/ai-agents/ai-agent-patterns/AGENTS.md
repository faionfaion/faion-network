---
slug: ai-agent-patterns
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Fundamental control flow patterns for AI agents.
content_id: "ae3d45909ea9b747"
tags: [agents, patterns, frameworks, orchestration]
---
# AI Agent Patterns

## Summary

**One-sentence:** Fundamental control flow patterns for AI agents.

**One-paragraph:** Fundamental control flow patterns for AI agents. Chain of Thought (CoT) for reasoning-only tasks, ReAct (Reason + Act) for tool-dependent work, Plan-and-Execute for multi-step projects, Tool Use Pattern for framework-based agents. Framework selection (LangGraph, AutoGen, CrewAI, OpenAI Agents SDK) depends on pattern complexity.

## Applies If (ALL must hold)

- Choosing a control flow pattern (CoT, ReAct, Plan-and-Execute) for a new agent task
- Explaining why a single prompt-response fails and what pattern would address the gap
- Selecting a framework (LangGraph, AutoGen, CrewAI, OpenAI Agents SDK) for a new agent project
- Debugging an agent that loops, hallucinates, or fails to use tools correctly where pattern mismatch is often the root cause

## Skip If (ANY kills it)

- Tasks solvable in a single LLM call where adding an agent pattern introduces latency and token overhead with no benefit
- Creative generation tasks where strict control flow degrades output quality
- When the framework dependency cost exceeds the project lifetime (e.g., a one-off script using LangGraph)
- Hard real-time tasks where multi-iteration loops are too slow (under 500 milliseconds SLA)

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
