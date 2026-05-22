---
slug: mcp-client-integration
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an MCP-client integration: agent host config (Claude Desktop / VS Code / custom Claude SDK) that launches MCP servers and exposes their tools to the model with same interface as native tools.
content_id: "65e69e810aee0bbb"
complexity: medium
produces: code
est_tokens: 3600
tags: [mcp, client, agent, claude-code, integration]
---
# MCP Client Integration — Agents, Claude Code, Host Configuration

## Summary

**One-sentence:** Produces an MCP-client integration: agent host config (Claude Desktop / VS Code / custom Claude SDK) that launches MCP servers and exposes their tools to the model with same interface as native tools.

**One-paragraph:** Produces an MCP-client integration. Agents consume MCP as clients: the host (Claude Desktop, VS Code, or a custom Claude SDK app) launches MCP servers and exposes their tools to the model. In a custom agent, the MCP Python or TypeScript SDK client connects to servers, lists tools, and forwards tool calls the model makes. The model sees MCP tools exactly like native SDK tools — no special handling needed downstream of the bridge.

**Ефективно для:** Бекенд-розробник для custom Claude SDK app — fixed client config з server launch + tool listing + bridge.

## Applies If (ALL must hold)

- Building a custom Claude SDK / Anthropic / OpenAI agent that needs MCP servers.
- Have ≥1 MCP server (third-party or own) to integrate.
- Host process can launch subprocesses (stdio) OR make HTTP+SSE calls.
- Tool catalogue is dynamic (servers add tools at runtime) OR static at startup.
- Have or can build a tool-bridge layer mapping MCP→SDK-native tool schemas.

## Skip If (ANY kills it)

- Building an MCP server (use `mcp-architecture` + `mcp-security`).
- Pure provider-SDK tools with no MCP need — skip MCP overhead.
- Single hard-coded tool — direct SDK tool definition is leaner.
- Host does not support subprocess / HTTP+SSE — out of scope.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Server catalogue | yaml (per-server: command, args, env, transport) | ML lead |
| Host runtime | string (Claude Desktop / VS Code / custom) | decision |
| Auth requirements | yaml | security |
| Tool-bridge target schema | json | ML team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/mcp-architecture` | Server-side spec. |
| `geek/ai/ml-engineer/mcp-security` | Consent + audit requirements. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: register-servers → launch → list-tools → bridge → wire-consent. | ~700 |
| `content/06-decision-tree.xml` | essential | Branch: host type + bridge static vs dynamic. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Fill claude-desktop-config.json / mcp-client.py from server catalogue. |
| `bridge-schemas` | sonnet | Map MCP tool schemas to SDK-native tool schemas. |
| `debug-launch` | opus | Cross-process diagnostic when server fails to start. |

## Templates

| File | Purpose |
|------|---------|
| `templates/claude-desktop-config.json` | Claude Desktop / VS Code mcp servers config. |
| `templates/mcp-client-python.py` | Python MCP client + tool-bridge skeleton. |
| `templates/mcp-client-typescript.ts` | TS MCP client + tool-bridge skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mcp-client-integration.py` | Validate the client config (servers, transport, auth, bridge target). | Pre-merge of every MCP client config PR. |

## Related

- [[mcp-architecture]] — server-side spec.
- [[mcp-security]] — consent + audit.
- [[claude-api]] — provider SDK target.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks host type (Claude Desktop / VS Code / custom Claude SDK) and bridge mode (static at startup / dynamic).
