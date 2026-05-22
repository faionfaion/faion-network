---
slug: tool-use-function-calling
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Function calling enables LLMs to interact with external systems by generating structured JSON specifying which tool to call and with what parameters.
content_id: "231043d936033385"
tags: [function-calling, tool-use, agents, structured-output, openai, claude, gemini]
---
# Tool Use and Function Calling

## Summary

**One-sentence:** Function calling enables LLMs to interact with external systems by generating structured JSON specifying which tool to call and with what parameters.

**One-paragraph:** Function calling enables LLMs to interact with external systems by generating structured JSON specifying which tool to call and with what parameters. The LLM does not execute functions — it produces the call specification; your code executes it. Keep the tool catalogue per call to ≤20; use RAG-over-tools to select the relevant subset for larger catalogues. Always validate LLM-generated arguments before execution.

## Applies If (ALL must hold)

- Agent needs to fetch live data (weather, prices, user records) the LLM does not know.
- Workflow requires state changes: writing files, sending messages, creating DB records.
- Output must be structured JSON consumed downstream — tools enforce the schema.
- Building multi-step agentic loops where each step depends on real execution results.
- Connecting an LLM to internal APIs or microservices.

## Skip If (ANY kills it)

- Query is pure text reasoning with no external dependency (summarize, translate, brainstorm).
- Tool roundtrip latency is unacceptable and pre-fetched context would suffice.
- LLM tool-selection accuracy is low (<70%) — use structured output or hardcoded routing instead.
- Single, fully deterministic function is always called — skip LLM selection, call it directly.

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
