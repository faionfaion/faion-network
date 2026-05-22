---
slug: mcp-dev-prompts
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A library of LLM prompts covering the full MCP development lifecycle: creating servers, adding tools, designing resources, debugging connection and execution failures, validating JSON-RPC messages, designing multi-server architectures, security review, performance optimization, test generation, and documentation.
content_id: "f0c06cb3de955c38"
tags: [mcp, prompts, development, debugging, templates]
---
# MCP Development Prompts — Server, Debug, Architecture, and Testing

## Summary

**One-sentence:** A library of LLM prompts covering the full MCP development lifecycle: creating servers, adding tools, designing resources, debugging connection and execution failures, validating JSON-RPC messages, designing multi-server architectures, security review, performance optimization, test generation, and documentation.

**One-paragraph:** A library of LLM prompts covering the full MCP development lifecycle: creating servers, adding tools, designing resources, debugging connection and execution failures, validating JSON-RPC messages, designing multi-server architectures, security review, performance optimization, test generation, and documentation.

## Applies If (ALL must hold)

- Starting a new MCP server from scratch — use the Create MCP Server prompt.
- Adding a new tool to an existing server — use the Add Tool prompt.
- Debugging a connection failure or tool execution error in MCP.
- Designing a multi-server MCP architecture for a system with multiple domains.
- Security review of an MCP server before production promotion.
- Generating test suites or documentation for an MCP server.

## Skip If (ANY kills it)

- When you already have working MCP code — these are scaffolding prompts, not refactoring prompts.

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
