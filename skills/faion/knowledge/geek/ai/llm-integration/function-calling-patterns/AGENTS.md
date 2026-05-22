---
slug: function-calling-patterns
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production patterns for LLM tool use: parallel execution of independent tool calls, a tool router that dispatches queries to the correct tool subset, an agentic loop with bounded iteration count, and argument validation before execution.
content_id: "927ab42d24484c9c"
tags: [tool-use, function-calling, agentic-loops, agent-safety, structured-output]
---
# Function Calling Patterns

## Summary

**One-sentence:** Production patterns for LLM tool use: parallel execution of independent tool calls, a tool router that dispatches queries to the correct tool subset, an agentic loop with bounded iteration count, and argument validation before execution.

**One-paragraph:** Production patterns for LLM tool use: parallel execution of independent tool calls, a tool router that dispatches queries to the correct tool subset, an agentic loop with bounded iteration count, and argument validation before execution. Covers both Anthropic (tool_use / tool_result blocks) and OpenAI (tool_calls in assistant message) formats.

## Applies If (ALL must hold)

- Agent must take actions in external systems (APIs, databases, file system).
- Structured data extraction from unstructured text with guaranteed JSON schema.
- Orchestrating parallel I/O-bound tool calls to reduce latency.
- Building multi-step agentic loops where the LLM decides the next action.
- Replacing prompt-based output parsing with schema-enforced tool use.

## Skip If (ANY kills it)

- Simple Q&A where no external action is needed — tool use adds tokens and latency.
- When all tools have side effects and the task is exploratory — use read-only tools first.
- More than ~20 tools in a single call — model selection accuracy degrades; use routing or subsets.
- Structured output purely for cosmetic formatting — prefer response_format or prefill.

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
