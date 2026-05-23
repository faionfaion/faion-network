# Model Context Protocol — Architecture and Core Primitives

## Summary

**One-sentence:** Produces an MCP architecture spec naming server primitives (tools / resources / prompts), transport (stdio / HTTP+SSE / WebSocket), and host integration boundaries per spec version 2025-11-25.

**One-paragraph:** Produces an MCP architecture spec. MCP is an open standard enabling seamless integration between LLM applications and external data sources and tools — a universal interface for reading files, executing functions, and handling contextual prompts via JSON-RPC 2.0 over stateful sessions. Protocol version 2025-11-25. Governance: Linux Foundation (Agentic AI Foundation). Spec covers server primitives (tools, resources, prompts), transports (stdio / HTTP+SSE), and host integration boundaries.

**Ефективно для:** Архітектор перед MCP server impl — fixed spec з primitives + transport + host integration.

## Applies If (ALL must hold)

- Designing an MCP server OR an MCP-host integration.
- Need to expose data / tools to multiple LLM hosts (Claude Desktop, VS Code, custom).
- Stateful session model (not one-shot REST) is appropriate for the integration.
- Compliance / audit demands a documented integration surface.
- JSON-RPC 2.0 over stdio / HTTP+SSE acceptable transports.

## Skip If (ANY kills it)

- Single-host single-tool integration — direct function-calling via SDK is leaner.
- Stateless REST or GraphQL adequate — MCP overhead unjustified.
- Need real-time bi-directional streaming — MCP sampling not designed for it.
- Host does not support MCP — direct SDK tool-calling.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use case: data + tools exposed | markdown | product |
| Host catalogue | list | ML lead |
| Transport policy | yaml | infra |
| Auth requirement | yaml | security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/mcp-security` | Security boundary required by MCP architecture. |
| `geek/ai/ml-engineer/mcp-client-integration` | Downstream integration methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: name-primitives → pick-transport → define-auth → version-protocol → write-spec. | ~700 |
| `content/05-examples.xml` | medium | Worked example: file-system MCP server with tools + resources. | ~600 |
| `content/06-decision-tree.xml` | essential | Transport branch + primitive choice. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Fill spec template from primitive list. |
| `design-primitives` | sonnet | Decide tools vs resources vs prompts per feature. |
| `debug-protocol` | opus | JSON-RPC negotiation / version mismatch triage. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mcp-spec.md` | Spec skeleton: primitives + transport + auth + versions. |
| `templates/mcp-server-python.py` | Python MCP server skeleton via official SDK. |
| `templates/mcp-server-typescript.ts` | TS MCP server skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mcp-architecture.py` | Validate the architecture spec (primitives, transport, version, auth). | Pre-merge of every MCP spec PR. |

## Related

- [[mcp-security]] — security boundary.
- [[mcp-client-integration]] — host side.
- [[mcp-dev-prompts]] — dev prompt library.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks transport (stdio for local desktop hosts, HTTP+SSE for remote / multi-tenant) and primitive types per feature.
