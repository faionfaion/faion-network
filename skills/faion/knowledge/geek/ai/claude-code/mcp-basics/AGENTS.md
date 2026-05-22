---
slug: mcp-basics
tier: geek
group: ai
domain: claude-code
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: 5-minute MCP basics primer + minimal stdio server scaffold (TypeScript / Python) producing a single typed tool.
content_id: "0fb5971129b24c53"
complexity: light
produces: spec
est_tokens: 4400
tags: [mcp, basics, getting-started, server-development, integrations]
---
# MCP Basics: Model Context Protocol Server Development

## Summary

**One-sentence:** 5-minute MCP basics primer + minimal stdio server scaffold (TypeScript / Python) producing a single typed tool.

**One-paragraph:** MCP basics is the entrypoint methodology: a 5-minute scaffold from `npm init` (or Python equivalent) to a working MCP server exposing a single typed tool the agent can call. It is the prerequisite for anyone hitting the deeper `mcp` (server-development) methodology. Output is a runnable repository with one tool, schema, README, and a `claude mcp add` install command.

**Ефективно для:**

- Перший MCP сервер: 5-хвилинний getting-started з мінімумом понять.
- ML / data engineer wraps ML inference у MCP — typed interface від першого виклику.
- Заміна curl/Bash виклику на named MCP tool, доступний усім агентам команди.
- Розподілення через npm / PyPI — installable за одну команду.

## Applies If (ALL must hold)

- First MCP server (no existing one in the team).
- Need a typed interface between agents and an internal system.
- Volume justifies the upfront 30-60 min scaffold (≥ 50 calls/week to the integration).

## Skip If (ANY kills it)

- A public MCP server covers the integration — prefer `npx -y @existing/package`.
- Single-use task where WebFetch / Bash is simpler.
- Server needs stateful sessions (stdio creates fresh process per session).
- Sub-10ms latency is required per call.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Node ≥ 18 or Python ≥ 3.10 | runtime | system |
| Service API + auth model | doc | service team |
| One tool spec | name + input + output | use-case |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: scaffold-one-tool-first, stdio-default-transport, schema-on-the-one-tool, install-command-in-readme, smoke-test-with-inspector | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `init-package` | haiku | Mechanical scaffold. |
| `scaffold-one-tool` | sonnet | Schema + handler design. |
| `smoke-test` | haiku | Inspector run. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ts-server.ts` | Minimal TypeScript MCP server with one tool |
| `templates/py-server.py` | Minimal Python MCP server with one tool |
| `templates/install-readme.md` | README install-command template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mcp-basics.py` | Validate the spec artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[mcp]]
- [[mcp-servers]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
