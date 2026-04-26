# MCP Gateway Composition — Five-Server Threshold

## Summary

When an agent connects to **more than 5 MCP servers**, put a gateway in front and compose them via one of three patterns: **virtual server** (gateway exposes a curated subset of upstream tools as one logical server), **federation** (gateways consume gateways in a tree), or **per-client visibility** (gateway filters the tool list by user/role). The gateway centralizes auth, rate limiting, audit, namespace collision resolution, and tool-list trimming — without it, each client re-implements all five concerns and the agent's tool catalog explodes past the ~25-tool selection-accuracy cliff.

## Why

A flat list of MCP servers has three failure modes that compound: (1) **schema bloat** — 6 servers × ~10 tools each = 60 schemas in the system prompt every turn, burning thousands of tokens and tanking selection accuracy; (2) **namespace collisions** — every server ships its own `search` and `create_issue`, the model picks wrong; (3) **fan-out auth** — each client maintains N OAuth flows, audit trails, rate limits. A gateway collapses all three: one auth perimeter, one tool list (trimmed per client), one audit log. ContextForge, Lunar, MCPJungle, and the IBM Q1 2026 reference designs converge on this pattern as the production default once you cross the threshold.

## When To Use

- Agent connects to >5 MCP servers (or ≥3 from different vendors).
- Multi-tenant deployment where different users/roles need different tool subsets.
- Cross-team setup where namespace collisions are likely (`github.search` vs `linear.search`).
- Compliance requirement to centralize audit / rate limit / OAuth across tools.
- Tool catalog already breaks the ~25-tool selection-accuracy threshold — gateway can lazy-load toolkits.

## When NOT To Use

- Solo dev or single agent with 1–3 servers — gateway is overhead, not value.
- Single-vendor stack where all MCP servers ship from one team and namespaces are pre-coordinated.
- Hard latency budget where every hop matters and the tool surface is small.
- Prototype phase — get the agent working flat first, add the gateway when pain appears.

## Content

| File | What's inside |
|------|---------------|
| `content/01-three-patterns.xml` | Virtual server, federation, per-client visibility — when each fits and how they compose. |
| `content/02-five-server-threshold.xml` | The empirical threshold rule and the schema-bloat failure mode it prevents. |

## Templates

| File | Purpose |
|------|---------|
| `templates/virtual-server.yaml` | ContextForge-style virtual-server config bundling 3 backends with deny rules. |
