---
slug: mcp
tier: geek
group: ai
domain: claude-code
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Spec for custom MCP servers in TypeScript or Python: typed tools, schema generation, secure credentials, transport choice, eval gate.
content_id: "ceaf1e832545180b"
complexity: deep
produces: spec
est_tokens: 4400
tags: [mcp, server-development, integration, apis, databases]
---
# MCP Server Development Guide

## Summary

**One-sentence:** Spec for custom MCP servers in TypeScript or Python: typed tools, schema generation, secure credentials, transport choice, eval gate.

**One-paragraph:** Custom MCP servers expose internal APIs / databases / services as typed tools Claude agents can invoke directly. Misdesign — fat servers with 50+ tools, OAuth flows in stdio transport, ad-hoc credential passing — defeats the win MCP offers. This methodology codifies the per-tool design (Zod / Pydantic schema, structured description, single responsibility), the credential-handling rule (env vars + minimum-scope), the transport choice (stdio for local, streamable-http for remote), the tool-count cap (≤ 20 per server; split otherwise), and the eval gate before publish. Output is a server.ts / server.py + package metadata + a README + a smoke-test.

**Ефективно для:**

- Команди, які пишуть кастомні інтеграції з internal API / DB / ML pipelines — MCP standardizes interface.
- ML inference сервіс експозиш як named tool, не як curl-обгортку.
- Read-only DB tools з permission enforcement на server-level.
- Distribuyте через npm / PyPI — installable package для всієї команди.

## Applies If (ALL must hold)

- Need a custom typed interface between Claude agents and an internal system.
- Service has no existing well-maintained public MCP server.
- Team standardizes tool surface across multiple agents.

## Skip If (ANY kills it)

- Public MCP server exists for the service — prefer `npx -y @package/name`.
- Single-use one-off script — direct Bash/WebFetch is faster.
- Service requires interactive OAuth (MCP servers run non-interactively).
- Sub-100ms latency required per call (stdio transport adds 10-50ms).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Service API doc | OpenAPI / SDK README | service team |
| Tool list | list of operations to expose | agent use-case spec |
| Credentials path | env-var convention + scope-min principle | security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[tool-description-as-prompt]] | upstream context required for this methodology |
| [[verb-object-tool-naming]] | upstream context required for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: tools-count-cap, schema-on-every-tool, transport-choice-explicit, credentials-via-env-vars, smoke-test-before-publish | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scope-the-server` | sonnet | Decision on tool set + split. |
| `scaffold` | haiku | Template fill. |
| `implement-tools` | sonnet | Per-tool schema + impl. |
| `smoke-test` | haiku | Mechanical eval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/server.ts` | TypeScript MCP server skeleton (stdio transport) |
| `templates/server.py` | Python MCP server skeleton (stdio transport) |
| `templates/server-remote.ts` | TypeScript MCP server skeleton (streamable-http) |
| `templates/install-cmd.md` | claude mcp add command with env-var passing template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mcp.py` | Validate the spec artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[mcp-basics]]
- [[mcp-servers]]
- [[tool-description-as-prompt]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
