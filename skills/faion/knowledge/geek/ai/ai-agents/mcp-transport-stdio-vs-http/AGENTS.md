# MCP Transport — stdio Local, Streamable HTTP Remote, SSE Dead

## Summary

Pick MCP transport from a closed three-option list keyed to deployment shape: **stdio** for local single-user subprocess servers (Claude Desktop, Claude Code, Cursor, IDE plugins), **Streamable HTTP** (single endpoint, OAuth 2.1, resumable streams) for remote/multi-tenant/hosted, and treat **SSE** as deprecated — only support it for back-compat with pre-`2026-03-26` clients. The choice is not a preference, it is dictated by whether the server runs as a subprocess of the client or behind a load balancer.

## Why

The MCP spec moved decisively: revision `2025-11-25` removed the dual-endpoint SSE transport in favor of a single Streamable HTTP endpoint that can negotiate POST → SSE upgrade per request. stdio remains the cheapest, lowest-latency option for local IPC because there is no HTTP framing, no OAuth handshake, and the lifecycle is tied to the parent process. Picking SSE in 2026 means writing dead-on-arrival code; picking stdio for a multi-tenant SaaS means you cannot horizontally scale (one process per client). Getting this wrong bakes in a rewrite at the worst time — when you are trying to go to production.

## When To Use

- Designing a new MCP server and choosing how clients will reach it.
- Migrating an existing SSE server to the post-`2026-03-26` spec.
- Reviewing an MCP integration PR — flag any new SSE code as tech debt on day one.
- Sizing a deployment: stdio implies "1 process per agent session"; HTTP implies a fleet behind an LB.

## When NOT To Use

- Non-MCP tool integrations (plain HTTP APIs, gRPC) — this rule is MCP-specific.
- Pure prototype where the server runs once on the author's laptop and never ships — pick whatever is fastest to type.
- Clients that explicitly require SSE for back-compat and you control both sides — keep SSE only behind a feature flag with a sunset date.

## Content

| File | What's inside |
|------|---------------|
| `content/01-transport-decision.xml` | The three-option decision tree, per-option fit, and the SSE deprecation rule. |
| `content/02-deployment-shapes.xml` | What each transport implies for scaling, auth, and lifecycle; HTTP needs OAuth 2.1 + resumable streams. |

## Templates

| File | Purpose |
|------|---------|
| `templates/transport-decision.txt` | One-screen decision flow an engineer can paste into a design doc. |
