---
slug: mcp-basics
tier: geek
group: ai
domain: claude-code
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Learn to build Model Context Protocol (MCP) servers that expose internal systems as typed, discoverable tools for Claude agents.
content_id: "c529ded457346fca"
tags: [mcp, basics, getting-started, server-development, integrations]
---
# MCP Basics: Model Context Protocol Server Development

## Summary

**One-sentence:** Learn to build Model Context Protocol (MCP) servers that expose internal systems as typed, discoverable tools for Claude agents.

**One-paragraph:** Learn to build Model Context Protocol (MCP) servers that expose internal systems as typed, discoverable tools for Claude agents. MCP provides standardized interfaces, automatic schema validation, and secure credential handling—replacing ad-hoc shell commands with production-ready integrations.

## Applies If (ALL must hold)

- Building a reusable typed interface between Claude agents and an internal system (database, API, filesystem abstraction).
- Replacing ad-hoc Bash(curl:*) tool calls with a named, schema-validated MCP tool that other agents can discover.
- Creating a Python ML inference server so Claude agents can invoke models as named tools.
- Distributing a shared integration to a team via npm or PyPI — MCP servers are installable packages.

## Skip If (ANY kills it)

- An existing public MCP server covers the integration — prefer npx -y @existing/package over building from scratch.
- Single-use task where a direct WebFetch or Bash call is simpler and won't be reused.
- The server needs to maintain stateful sessions between tool calls — stdio transport creates a fresh process per session, no session affinity.
- Sub-10ms latency is required per tool call — MCP transport overhead is 10-50ms minimum.

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
