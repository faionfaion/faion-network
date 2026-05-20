---
slug: autonomous-agents
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Autonomous agents are LLM-powered systems that can independently plan, execute tasks, use tools, and iterate toward goals.
content_id: "cf089429781b5b57"
tags: [agents, react, planning, tool-use, orchestration]
---
# Autonomous Agents

## Summary

**One-sentence:** Autonomous agents are LLM-powered systems that can independently plan, execute tasks, use tools, and iterate toward goals.

**One-paragraph:** Autonomous agents are LLM-powered systems that can independently plan, execute tasks, use tools, and iterate toward goals. They combine reasoning, memory, and action capabilities to accomplish complex objectives with minimal human intervention through core patterns: ReAct (Reason + Act loop), Plan-and-Execute (planning first), and Reflexion (self-critique and improvement). Build them with hard iteration caps, idempotent tools, explicit terminal conditions, and human checkpoints for irreversible actions.

## Applies If (ALL must hold)

- Task requires 3+ sequential tool calls where each step depends on prior output.
- Workflow involves dynamic branching based on intermediate observations (e.g., search → read → decide → act).
- Goal is underspecified at start and requires iterative refinement (research, debugging, code generation with feedback loops).
- Automating knowledge work: data collection, analysis, report generation, competitive research.
- Code generation tasks that require run-fix-retry cycles (sandbox execution).
- Multi-source information synthesis requiring dynamic retrieval decisions.

## Skip If (ANY kills it)

- Single-turn tasks with deterministic output — just use a direct prompt.
- Latency-sensitive production paths (each ReAct loop adds 1-3 LLM calls).
- Structured ETL with known schema — a script beats an agent every time.
- Tasks with binary success/failure where hallucinated tool calls cause irreversible side effects (financial writes, database deletes).
- When you need reproducible deterministic output — agent non-determinism is a bug here.

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
