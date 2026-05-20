---
slug: websocket-design
tier: solo
group: dev
domain: api-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: WebSockets provide full-duplex persistent connections for real-time features.
content_id: "ee5b9ef5dab52421"
tags: [websocket, realtime, heartbeat, redis-pubsub, reconnect]
---
# WebSocket Design

## Summary

**One-sentence:** WebSockets provide full-duplex persistent connections for real-time features.

**One-paragraph:** WebSockets provide full-duplex persistent connections for real-time features. Define a versioned message envelope (`{v, type, channel, seq, ts, payload}`), implement heartbeat/ping-pong with server-side disconnect on missed beats, reconnect with exponential backoff and full jitter, and scale fan-out horizontally via Redis Pub/Sub or NATS.

## Applies If (ALL must hold)

- Server-pushed events at sub-second latency: chat, presence, live cursors, order book updates, multiplayer state.
- Bidirectional streams where the client also sends frequently (collab editing, voice control loops).
- High-frequency updates where polling would burn 10x bandwidth.
- LLM streaming when SSE is not enough (binary frames, two-way tool calls). Otherwise prefer SSE — simpler, proxy-friendly.
- Agent pipelines that need a long-lived control channel (workers reporting progress to a dashboard).

## Skip If (ANY kills it)

- One-shot CRUD or rare polls (every >5s) — REST is cheaper.
- Server-only push, no client→server traffic — SSE wins on simplicity, HTTP/2 multiplexing, and resume.
- Behind misconfigured proxies / corporate firewalls that strip Upgrade headers — fall back to SSE or long-poll.
- Mobile networks with aggressive NAT timeouts unless you commit to heartbeats and resumption.
- When you cannot run a stateful tier — pure serverless (Lambda) supports WS only via API Gateway, with state in DynamoDB.

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

- parent skill: `solo/dev/api-developer/`
