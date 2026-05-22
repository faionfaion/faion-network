---
slug: multi-agent-systems
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Multi-agent systems coordinate multiple AI agents to solve tasks that exceed a single agent's context, parallelism, or role boundaries.
content_id: "e22a48ce3324f96a"
tags: [agents, orchestration, langgraph, workflows, parallel-execution]
---
# Multi-Agent Systems

## Summary

**One-sentence:** Multi-agent systems coordinate multiple AI agents to solve tasks that exceed a single agent's context, parallelism, or role boundaries.

**One-paragraph:** Multi-agent systems coordinate multiple AI agents to solve tasks that exceed a single agent's context, parallelism, or role boundaries. Use the Claude Agent SDK's subagent primitive: parent spawns children with typed contracts, waits for structured results, routes to the next stage. Keep orchestrators stateless (routing only); push state to a shared file or queue.

## Applies If (ALL must hold)

- Task requires parallel specialized work: research + coding + review happening simultaneously
- Problem is too large for a single context window
- Workflow has natural role boundaries (planner, executor, critic, verifier)
- Iterative refinement loops benefit from adversarial agents (generator vs. critic)
- Long-running pipelines where intermediate outputs need validation checkpoints

## Skip If (ANY kills it)

- Simple, linear task a single agent completes in one pass
- Low latency required — multi-agent adds orchestration overhead (2-5x latency)
- Budget is tight — multiple agents multiply token spend
- Team lacks observability tooling — debugging multi-agent failures is hard without traces
- Task has tight coupling between steps where parallelization creates conflicts

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
