---
slug: agents-react-pattern
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: ReAct (Reason + Act) is the canonical single-agent loop: the LLM thinks, calls a tool, observes the result, and repeats until the task is done or an iteration cap is hit.
content_id: "ec663546d4646ae6"
tags: [agents, react, tool-use, llm, autonomous-agents]
---
# ReAct Agent Pattern — Reason + Act Loop Implementation

## Summary

**One-sentence:** ReAct (Reason + Act) is the canonical single-agent loop: the LLM thinks, calls a tool, observes the result, and repeats until the task is done or an iteration cap is hit.

**One-paragraph:** ReAct (Reason + Act) is the canonical single-agent loop: the LLM thinks, calls a tool, observes the result, and repeats until the task is done or an iteration cap is hit. It is adaptive and cheap compared to Plan-and-Execute — typically 50% fewer LLM calls for exploratory tasks — but requires hard iteration limits and explicit completion detection to avoid runaway loops.

## Applies If (ALL must hold)

- Task requires dynamic tool selection across multiple steps with branching based on intermediate results.
- Workflow involves research + synthesis + action that cannot be scripted in advance.
- Code generation and execution loops where the agent must test and fix iteratively.
- Multi-source data gathering where the number of sources is unknown upfront.
- Automation of knowledge work: writing, classification, extraction across variable-length inputs.

## Skip If (ANY kills it)

- Task is deterministic and mappable to a fixed pipeline — use a DAG, not an agent.
- Real-time response under 500ms is required — autonomous loop latency is incompatible.
- Actions are irreversible (send email, delete records, charge cards) without human approval — use Plan-and-Execute with approval gate instead.
- Cost budget is fixed and tight — ReAct loops can expand token usage 5-20x vs a single call.

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
