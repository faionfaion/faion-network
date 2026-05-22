---
slug: mcp-server-implementation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Implements an MCP server in TypeScript (McpServer + Zod) or Python (FastMCP / mcp.server) exposing tools, resources, and prompts with stdio or HTTP+SSE transport.
content_id: "28e453af2702718e"
complexity: deep
produces: code
est_tokens: 4300
tags: [mcp, server, fastmcp, typescript, python]
---
# MCP Server Implementation — TypeScript and Python

## Summary

**One-sentence:** Implements an MCP server in TypeScript (McpServer + Zod) or Python (FastMCP / mcp.server) exposing tools, resources, and prompts with stdio or HTTP+SSE transport.

**One-paragraph:** Implements an MCP server in TypeScript (McpServer + Zod) or Python (FastMCP / mcp.server) exposing tools, resources, and prompts with stdio or HTTP+SSE transport. The methodology assumes the inputs in Prerequisites and produces a `code` artefact validated by `scripts/validate-mcp-server-implementation.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** ML/AI engineers building reusable MCP tool servers shared across Claude Desktop, VS Code Copilot, and custom Claude SDK agents.

## Applies If (ALL must hold)

- Building a reusable tool server that multiple AI clients will share.
- Exposing database, filesystem, or external API access to agents without hardcoded tool code in the agent.
- Custom Claude Code agents (~/.claude/agents/) that need domain-specific tools.
- Any agent needing database, filesystem, or external API access without hardcoded tool code.

## Skip If (ANY kills it)

- Single-agent prototype with one or two tools — inline Claude SDK tool definitions are simpler.
- HTTP transport in environments without an auth layer — stdio trusts the local process by default; HTTP requires bearer token auth.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[mcp-architecture]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules with rationale and source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples for the output artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix. | ~800 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether the methodology applies, ending in rule refs. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-skeleton` | sonnet | Boilerplate + schema scaffolding. |
| `fill-business-logic` | opus | Domain-judgment-heavy core logic. |
| `lint-and-test` | haiku | Mechanical checks against the contract. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.py` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/skeleton.py` | Working code skeleton showing the produced shape with the contract types. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mcp-server-implementation.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[mcp-architecture]]
- [[mcp-security]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `mcp-server-implementation` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
