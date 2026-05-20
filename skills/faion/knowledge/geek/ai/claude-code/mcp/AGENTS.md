---
slug: mcp
tier: geek
group: ai
domain: claude-code
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Build custom MCP (Model Context Protocol) servers in TypeScript or Python to expose internal APIs, databases, and services as typed tools that Claude agents can invoke directly.
content_id: "f8b6c49825dce4a6"
tags: [mcp, server-development, integration, apis, databases]
---
# MCP Server Development Guide

## Summary

**One-sentence:** Build custom MCP (Model Context Protocol) servers in TypeScript or Python to expose internal APIs, databases, and services as typed tools that Claude agents can invoke directly.

**One-paragraph:** Build custom MCP (Model Context Protocol) servers in TypeScript or Python to expose internal APIs, databases, and services as typed tools that Claude agents can invoke directly. MCP provides standardized interfaces, automatic schema generation, and secure credential handling.

## Applies If (ALL must hold)

- Building a custom integration between Claude Code agents and an internal API, database, or service.
- The target service has no existing MCP server in the public catalog.
- Standardizing tool interfaces for a team: all agents use the same typed MCP tools instead of ad-hoc curl/Bash.
- Wrapping a Python ML pipeline so Claude agents can invoke model inference as a named tool.
- Creating a read-only database tool that enforces SELECT-only policy at the server level.

## Skip If (ANY kills it)

- A well-maintained public MCP server already exists for the service — prefer npx -y @package/name over building from scratch.
- The integration is a single-use one-off script — direct Bash/WebFetch is faster to write and maintain.
- The service requires complex OAuth flows that are interactive — MCP servers run non-interactively.
- You need sub-100ms latency for every tool call — MCP stdio transport adds approximately 10-50ms per call.

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

- parent skill: `geek/ai/claude-code/`
