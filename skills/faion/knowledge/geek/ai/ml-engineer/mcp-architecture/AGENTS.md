---
slug: mcp-architecture
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: MCP is an open standard enabling seamless integration between LLM applications and external data sources and tools.
content_id: "70658d41715d06b7"
tags: [mcp, llm, protocol, tools, integration]
---
# Model Context Protocol — Architecture and Core Primitives

## Summary

**One-sentence:** MCP is an open standard enabling seamless integration between LLM applications and external data sources and tools.

**One-paragraph:** MCP is an open standard enabling seamless integration between LLM applications and external data sources and tools. It provides a universal interface for reading files, executing functions, and handling contextual prompts via JSON-RPC 2.0 over stateful sessions. Protocol version 2025-11-25. Governance: Linux Foundation (Agentic AI Foundation). Adopters: Anthropic, OpenAI, Google DeepMind, Microsoft, AWS.

## Applies If (ALL must hold)

- Exposing internal tools (database queries, file system, APIs) to LLM hosts without custom integration per host.
- Building reusable tool servers that work across Claude Desktop, VS Code Copilot, and custom agents simultaneously.
- Giving agents access to resources that need app-controlled (not model-controlled) presentation of context.
- Standardizing tool interfaces across a team — one MCP server, many AI clients.
- Enabling sampling: MCP server needs to make LLM calls back through the host (avoids embedding API keys in servers).

## Skip If (ANY kills it)

- Simple single-purpose agent that only needs 1-2 hardcoded tool functions — direct SDK tool definitions are simpler.
- Latency-critical paths — MCP stdio transport adds ~5-20ms per round trip; HTTP transport adds network overhead.
- Teams without TypeScript or Python experience — MCP SDK requires one of these; no other mature options.
- Environments where stdio process management is unreliable (some containerized setups need explicit lifecycle management).
- When the tool surface changes frequently — MCP server restarts are required to reload tool definitions in most clients.

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
