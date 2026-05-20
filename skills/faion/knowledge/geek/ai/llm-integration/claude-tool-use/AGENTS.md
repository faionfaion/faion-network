---
slug: claude-tool-use
tier: geek
group: ai
domain: llm-integration
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for Claude's tool use (function calling): defining tools with JSON Schema `input_schema`, detecting `stop_reason == "tool_use"`, running the canonical agentic loop, forcing structured JSON output via `tool_choice`, and building custom MCP servers.
content_id: "0a55c5dba8f761d5"
tags: [claude, tool-use, function-calling, agent-loop, mcp]
---
# Claude Tool Use

## Summary

**One-sentence:** Patterns for Claude's tool use (function calling): defining tools with JSON Schema `input_schema`, detecting `stop_reason == "tool_use"`, running the canonical agentic loop, forcing structured JSON output via `tool_choice`, and building custom MCP servers.

**One-paragraph:** Patterns for Claude's tool use (function calling): defining tools with JSON Schema `input_schema`, detecting `stop_reason == "tool_use"`, running the canonical agentic loop, forcing structured JSON output via `tool_choice`, and building custom MCP servers. The core rule: always append the full `response.content` list (not just text) as the assistant turn — omitting tool_use blocks from history causes API errors on the next turn.

## Applies If (ALL must hold)

- Agent loops where Claude must call external functions and incorporate results.
- Forcing typed structured JSON output from Claude (tool-choice trick).
- Extracting typed data from unstructured text using a schema-constrained call.
- Parallel tool dispatch — Claude can request multiple tools in one response.
- MCP server integration for Claude Desktop agents needing filesystem, GitHub, or DB access.

## Skip If (ANY kills it)

- Simple text generation with no external data needs — tool definitions inflate prompt and cost tokens.
- When OpenAI Structured Outputs or Gemini `response_schema` are already in use — mixing SDKs adds complexity.
- Real-time streaming responses — tool use requires a complete response before the loop can continue.
- Tool set larger than ~20 tools — Claude may pick the wrong tool; use tool routing to reduce the visible set.

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
