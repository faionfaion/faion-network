---
slug: mcp-servers
tier: geek
group: ai
domain: claude-code
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reference catalog of 40+ popular MCP servers for Claude Code, organized by service category (marketing, analytics, project management, development, design, etc.
content_id: "ee844a3dbd5c85e6"
tags: [mcp, claude-code, integration, api, tools]
---
# MCP Server Catalog

## Summary

**One-sentence:** Reference catalog of 40+ popular MCP servers for Claude Code, organized by service category (marketing, analytics, project management, development, design, etc.

**One-paragraph:** Reference catalog of 40+ popular MCP servers for Claude Code, organized by service category (marketing, analytics, project management, development, design, etc.). Includes setup commands, authentication requirements, and best practices for agent integration.

## Applies If (ALL must hold)

- Agent needs to interact with an external service (GitHub, Slack, Notion, Stripe) without writing custom API code.
- Standardizing tool interfaces across multiple agents — all agents use the same MCP tool, not ad-hoc curl calls.
- Replacing fragile shell-script API wrappers with a typed, introspectable MCP interface.
- Enabling Claude Code to read from or write to databases, CRMs, or project management tools mid-session.

## Skip If (ANY kills it)

- The service has no MCP server and the task is one-off — use WebFetch + Bash(curl) directly instead.
- The MCP server requires an OAuth flow that cannot be completed non-interactively — authentication will block.
- Security policy disallows external process spawning or network calls from within Claude Code.
- The catalog server's tool count is very large (>50 tools) — it pollutes the model's tool namespace; filter or build a focused custom server instead.

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
