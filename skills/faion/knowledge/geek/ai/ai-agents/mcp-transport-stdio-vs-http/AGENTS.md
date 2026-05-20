---
slug: mcp-transport-stdio-vs-http
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Pick MCP transport from a closed three-option list keyed to deployment shape: stdio for local single-user subprocess servers (Claude Desktop, Claude Code, Cursor, IDE plugins), Streamable HTTP (single endpoint, OAuth 2.
content_id: "e32177a1a91624a0"
tags: [mcp, transport, deployment, architecture, scaling]
---
# MCP Transport — stdio Local, Streamable HTTP Remote, SSE Dead

## Summary

**One-sentence:** Pick MCP transport from a closed three-option list keyed to deployment shape: stdio for local single-user subprocess servers (Claude Desktop, Claude Code, Cursor, IDE plugins), Streamable HTTP (single endpoint, OAuth 2.

**One-paragraph:** Pick MCP transport from a closed three-option list keyed to deployment shape: stdio for local single-user subprocess servers (Claude Desktop, Claude Code, Cursor, IDE plugins), Streamable HTTP (single endpoint, OAuth 2.1, resumable streams) for remote/multi-tenant/hosted, and treat SSE as deprecated — only support it for back-compat with pre-2026-03-26 clients. The choice is not a preference, it is dictated by whether the server runs as a subprocess of the client or behind a load balancer.

## Applies If (ALL must hold)

- Designing a new MCP server and choosing how clients will reach it.
- Migrating an existing SSE server to the post-2026-03-26 spec.
- Reviewing an MCP integration PR — flag any new SSE code as tech debt on day one.
- Sizing a deployment: stdio implies "1 process per agent session"; HTTP implies a fleet behind an LB.

## Skip If (ANY kills it)

- Non-MCP tool integrations (plain HTTP APIs, gRPC) — this rule is MCP-specific.
- Pure prototype where the server runs once on the author's laptop and never ships — pick whatever is fastest to type.
- Clients that explicitly require SSE for back-compat and you control both sides — keep SSE only behind a feature flag with a sunset date.

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

- parent skill: `geek/ai/ai-agents/`
