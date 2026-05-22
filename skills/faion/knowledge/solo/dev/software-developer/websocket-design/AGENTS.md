---
slug: websocket-design
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: WebSocket provides full-duplex, persistent connections between clients and servers.
content_id: "ee5b9ef5dab52421"
tags: [websocket, real-time, networking, server-push, scalability]
---
# WebSocket Design

## Summary

**One-sentence:** WebSocket provides full-duplex, persistent connections between clients and servers.

**One-paragraph:** WebSocket provides full-duplex, persistent connections between clients and servers. Core rule: authenticate on the upgrade handshake before accepting the connection, implement heartbeats below the load-balancer idle timeout, and reconnect with exponential backoff plus jitter on the client side.

## Applies If (ALL must hold)

- Real-time UI features: chat, presence indicators, live cursors, notification feeds
- Server-pushed updates where polling burns requests (price tickers, game state, dashboards)
- Bidirectional protocols (collaborative editing, low-latency RPC) where SSE alone is insufficient
- Frontends needing one persistent connection multiplexed across many topics per user

## Skip If (ANY kills it)

- One-way server-to-client streams — use Server-Sent Events; simpler, works through more proxies
- Request/response-style RPC — use HTTP/gRPC; WebSockets add framing overhead and connection state
- Behind aggressive corporate proxies that strip WebSocket upgrades — fall back to long-polling
- Serverless platforms without WS support — use AWS API Gateway WebSockets or Cloudflare Durable Objects

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

- parent skill: `solo/dev/software-developer/`
