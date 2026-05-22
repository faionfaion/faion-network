---
slug: mcp-client-integration
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Agents consume MCP as clients: the host (Claude Desktop, VS Code, or custom Claude SDK app) launches MCP servers and exposes their tools to the model.
content_id: "5278b7336d2ed7be"
tags: [mcp, client, agent, claude-code, integration]
---
# MCP Client Integration — Agents, Claude Code, and Host Configuration

## Summary

**One-sentence:** Agents consume MCP as clients: the host (Claude Desktop, VS Code, or custom Claude SDK app) launches MCP servers and exposes their tools to the model.

**One-paragraph:** Agents consume MCP as clients: the host (Claude Desktop, VS Code, or custom Claude SDK app) launches MCP servers and exposes their tools to the model. In a custom agent, use the MCP Python or TypeScript SDK client to connect to servers, list tools, and forward tool calls the model makes. The model sees MCP tools exactly like native SDK tools — no special handling needed.

## Applies If (ALL must hold)

- Custom agent that needs to connect programmatically to MCP servers to discover and invoke tools.
- Claude Code or Claude Desktop setup needing to register local or remote MCP servers.
- Agent that needs to read resources (files, database schemas) provided by an MCP server.
- Building a host application that orchestrates multiple MCP servers.

## Skip If (ANY kills it)

- When the host (Claude Desktop, VS Code) already handles MCP connections — you only need to add the server to the host config JSON, not write client code.
- Agent with inline tool definitions that do not need to span multiple hosts — MCP client overhead is not justified.

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
