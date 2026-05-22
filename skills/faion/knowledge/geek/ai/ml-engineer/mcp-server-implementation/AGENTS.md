---
slug: mcp-server-implementation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Build MCP servers using the official TypeScript SDK (McpServer + Zod) or Python SDK (FastMCP for rapid development, mcp.
content_id: "28e453af2702718e"
tags: [mcp, server, fastmcp, typescript, python]
---
# MCP Server Implementation — TypeScript and Python

## Summary

**One-sentence:** Build MCP servers using the official TypeScript SDK (McpServer + Zod) or Python SDK (FastMCP for rapid development, mcp.

**One-paragraph:** Build MCP servers using the official TypeScript SDK (McpServer + Zod) or Python SDK (FastMCP for rapid development, mcp.server for low-level control). Servers expose tools, resources, and prompts. stdio transport is the default; HTTP+SSE is used for multi-client scenarios.

## Applies If (ALL must hold)

- Building a reusable tool server that multiple AI clients will share.
- Exposing database, filesystem, or external API access to agents without hardcoded tool code in the agent.
- Custom Claude Code agents (~/.claude/agents/) that need domain-specific tools.
- Any agent needing database, filesystem, or external API access without hardcoded tool code.

## Skip If (ANY kills it)

- Single-agent prototype with one or two tools — inline Claude SDK tool definitions are simpler.
- HTTP transport in environments without an auth layer — stdio trusts the local process by default; HTTP requires bearer token auth.

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
