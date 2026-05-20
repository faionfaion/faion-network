---
slug: model-context-protocol
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Model Context Protocol is an open standard for connecting LLMs to external tools and data sources without custom SDK integration per tool.
content_id: "964126af4ae0af78"
tags: [mcp, tools, protocol, integration, standardization]
---
# MCP (Model Context Protocol)

## Summary

**One-sentence:** Model Context Protocol is an open standard for connecting LLMs to external tools and data sources without custom SDK integration per tool.

**One-paragraph:** Model Context Protocol is an open standard for connecting LLMs to external tools and data sources without custom SDK integration per tool. MCP decouples tool versioning from agent versioning and provides reusable, composable tool definitions across multiple clients.

## Applies If (ALL must hold)

- You need to expose tools, resources, or data sources to Claude or other MCP clients via a standardized protocol without custom SDK integration per tool.
- Building a reusable tool server that multiple agents or clients can consume without duplicating integration code.
- The tool set is maintained separately from the agent code — MCP decouples tool versioning from agent versioning.
- You want Claude Code to access project-specific tools (databases, APIs, file systems) without per-project SDK configuration.
- Integrating with existing MCP ecosystem servers (Brave Search, PostgreSQL, GitHub, filesystem) that are already MCP-compliant.

## Skip If (ANY kills it)

- The agent runs in a fully sandboxed environment with no external communication — MCP requires a transport layer (stdio or SSE).
- You only need one-time tool use for a single agent — direct LangChain/LlamaIndex tool definition is simpler for non-shared tools.
- The tool response is a binary stream (audio, video) — MCP currently handles text/JSON tool results; binary data requires base64 encoding.
- Latency is critical under 100ms — stdio transport adds process spawn overhead; SSE adds network round-trip.
- You need bidirectional streaming during tool execution — MCP tool calls are request/response, not streaming mid-call.

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
