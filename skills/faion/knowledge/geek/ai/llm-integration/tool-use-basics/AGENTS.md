---
slug: tool-use-basics
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Enables LLMs to call external functions, APIs, and code by defining a tool registry (name → callable), converting it to provider-specific JSON schema, and running a request-execute-respond loop with a hard iteration cap.
content_id: "e4738d1508fe609c"
tags: [tool-use, function-calling, agent-loop, openai, anthropic]
---
# Tool Use Basics

## Summary

**One-sentence:** Enables LLMs to call external functions, APIs, and code by defining a tool registry (name → callable), converting it to provider-specific JSON schema, and running a request-execute-respond loop with a hard iteration cap.

**One-paragraph:** Enables LLMs to call external functions, APIs, and code by defining a tool registry (name → callable), converting it to provider-specific JSON schema, and running a request-execute-respond loop with a hard iteration cap. Covers OpenAI function calling and Anthropic tool use patterns.

## Applies If (ALL must hold)

- Accessing real-time or external data (weather, stocks, database records, web search)
- Precise computation required (math, date arithmetic, aggregation) where LLMs hallucinate
- Autonomous agents taking actions (file writes, API calls, messages) in multi-step workflows
- ReAct-style (Reason + Act) loops where the model iterates until a goal is achieved
- Grounding LLM responses in authoritative data sources rather than training knowledge

## Skip If (ANY kills it)

- Task solvable with a single in-context prompt — tool calling adds latency and complexity
- All required information is already in the prompt context
- Destructive tools (delete, send emails, charge money) with no human approval gate
- Small/fast models (Haiku, gpt-4o-mini) with complex schemas (>5 tools, nested params) — selection accuracy degrades

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

- parent skill: `geek/ai/llm-integration/`
