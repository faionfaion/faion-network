---
slug: mcp-gateway-composition
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When an agent connects to more than 5 MCP servers, put a gateway in front and compose them via one of three patterns: virtual server (gateway exposes a curated subset of upstream tools as one logical server), federation (gateways consume gateways in a tree), or per-client visibility (gateway filters the tool list by user/role).
content_id: "013755a50114a6c6"
tags: [mcp, tool-composition, gateway-patterns, multi-server, scaling]
---
# MCP Gateway Composition — Five-Server Threshold

## Summary

**One-sentence:** When an agent connects to more than 5 MCP servers, put a gateway in front and compose them via one of three patterns: virtual server (gateway exposes a curated subset of upstream tools as one logical server), federation (gateways consume gateways in a tree), or per-client visibility (gateway filters the tool list by user/role).

**One-paragraph:** When an agent connects to more than 5 MCP servers, put a gateway in front and compose them via one of three patterns: virtual server (gateway exposes a curated subset of upstream tools as one logical server), federation (gateways consume gateways in a tree), or per-client visibility (gateway filters the tool list by user/role). The gateway centralizes auth, rate limiting, audit, namespace collision resolution, and tool-list trimming — without it, each client re-implements all five concerns and the agent's tool catalog explodes past the ~25-tool selection-accuracy cliff.

## Applies If (ALL must hold)

- Agent connects to >5 MCP servers (or ≥3 from different vendors).
- Multi-tenant deployment where different users/roles need different tool subsets.
- Cross-team setup where namespace collisions are likely (github.search vs linear.search).
- Compliance requirement to centralize audit / rate limit / OAuth across tools.
- Tool catalog already breaks the ~25-tool selection-accuracy threshold — gateway can lazy-load toolkits.

## Skip If (ANY kills it)

- Solo dev or single agent with 1–3 servers — gateway is overhead, not value.
- Single-vendor stack where all MCP servers ship from one team and namespaces are pre-coordinated.
- Hard latency budget where every hop matters and the tool surface is small.
- Prototype phase — get the agent working flat first, add the gateway when pain appears.

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
