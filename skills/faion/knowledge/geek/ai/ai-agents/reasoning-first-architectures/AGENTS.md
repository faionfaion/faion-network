---
slug: reasoning-first-architectures
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Agents that act before thinking produce suboptimal outcomes.
content_id: "69084dee94f28ecc"
tags: [agent-reasoning, think-before-act, react, tree-of-thought, reflexion]
---
# Reasoning-First Architectures

## Summary

**One-sentence:** Agents that act before thinking produce suboptimal outcomes.

**One-paragraph:** Agents that act before thinking produce suboptimal outcomes. Use reasoning-first patterns (ReAct, Tree-of-Thought, Reflexion, Planning Loops, Critique-and-Revise) to separate thinking from action. Each pattern trades off latency, cost, and quality differently.

## Applies If (ALL must hold)

- Tasks where acting without a plan produces low-quality output (complex coding, multi-step math, strategic decisions)
- Research synthesis where the agent must reconcile conflicting sources before concluding
- Any agentic pipeline where premature tool calls cause cascading errors (e.g. writing code before understanding the full spec)
- Quality-critical generation where a Critique-and-Revise loop demonstrably improves output
- Problems with multiple viable solution paths where Tree-of-Thought search yields better solutions than greedy selection

## Skip If (ANY kills it)

- Simple factual retrieval where reasoning adds latency with no quality gain
- Latency-sensitive paths (<500ms budget) — extended thinking and multi-path search are expensive
- Tasks where the domain is so narrow that chain-of-thought adds no signal (e.g. regex matching, format conversion)
- Reflexion loops on tasks with no verifiable exit criterion — the loop runs to the cap and exits with no quality guarantee
- Streaming response use cases where intermediate reasoning steps must not be shown to the user

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
