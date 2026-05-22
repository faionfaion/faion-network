---
slug: mcp-transport-stdio-vs-http
tier: geek
group: ai
domain: ai-agents
version: 2.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Picks MCP transport (stdio for local subprocess, Streamable HTTP for remote/multi-tenant) and emits a transport-spec.
content_id: 15ec05cb9a04dde0
complexity: medium
produces: spec
est_tokens: 4000
tags: [mcp, transport, stdio, streamable-http, oauth]
---
# Mcp Transport Stdio Vs Http

## Summary

**One-sentence:** Picks MCP transport (stdio for local subprocess, Streamable HTTP for remote/multi-tenant) and emits a transport-spec.

**One-paragraph:** MCP transport choice is not preference — it's dictated by deployment shape. stdio for single-user subprocess servers; Streamable HTTP (with OAuth 2.1 and resumable streams) for remote / multi-tenant / hosted. SSE is deprecated. This methodology turns a deployment profile into a deterministic transport-spec.

**Ефективно для:** solopreneur publishing an MCP server who needs the right transport at launch.

## Applies If (ALL must hold)

- Building or shipping an MCP server.
- Deployment shape known (laptop subprocess vs hosted multi-tenant).
- ≥1 client target known (Claude Desktop, Claude Code, Cursor, IDE, web).
- Auth requirements known (none, OAuth 2.1, API key).
- Network constraints known (NAT'd, firewalled, public).

## Skip If (ANY kills it)

- Server architecture mandates a specific transport already.
- Not building an MCP server — different methodology.
- Internal-only on a fixed VPN — pick HTTP unconditionally.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `deployment-profile.yaml` | client_targets, multi_tenant, auth_required, network_constraints | author |
| `MCP SDK` | py/ts | code |
| `Auth provider (if HTTP)` | Auth0/Cognito/etc | infra |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[mcp-resource-vs-tool-vs-prompt]] | Primitive classification depends on transport feasibility. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules for stdio vs streamable HTTP, deprecation of SSE, OAuth 2.1 mandate. | ~1000 |
| `content/02-output-contract.xml` | essential | transport-spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Stdio over network, SSE for new builds, HTTP without OAuth, resumable disabled. | ~700 |
| `content/04-procedure.xml` | recommended | 5-step selection procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/deployment-profile.yaml` | Input. |
| `templates/transport-spec.md` | Output. |
| `templates/server_http.py` | Working Streamable HTTP scaffold. |
| `templates/server_stdio.py` | Working stdio scaffold. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-mcp-transport-stdio-vs-http.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

- [[mcp-gateway-composition]]
- [[mcp-resource-vs-tool-vs-prompt]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on multi_tenant (true → streamable-http; false → stdio), then on auth_required (true with http → OAuth 2.1 mandatory), then on resumable_streams (always true for streamable-http). Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
