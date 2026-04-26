# WebSocket Design

## Summary

WebSockets provide full-duplex persistent connections for real-time features. Define a versioned message envelope (`{v, type, channel, seq, ts, payload}`), implement heartbeat/ping-pong with server-side disconnect on missed beats, reconnect with exponential backoff and full jitter, and scale fan-out horizontally via Redis Pub/Sub or NATS.

## Why

Without heartbeats, stale connections accumulate silently until the server runs out of file descriptors. Without jitter on reconnect, a deploy redeploys all clients simultaneously, creating a thundering herd that DDoSes the auth endpoint. Without Redis Pub/Sub, WebSocket connections are pinned to one process and fan-out breaks under horizontal scaling.

## When To Use

- Real-time features at sub-second latency: chat, presence, live cursors, order book updates
- Bidirectional streams where the client also sends frequently (collab editing, gaming)
- High-frequency updates where polling would burn 10x bandwidth
- Agent pipelines needing a long-lived control channel (workers reporting progress)

## When NOT To Use

- One-shot CRUD or rare polls (every >5s) — REST is cheaper
- Server-only push without client traffic — SSE is simpler and proxy-friendly
- Behind misconfigured proxies/firewalls that strip `Upgrade` headers
- Pure serverless (Lambda) unless using API Gateway WS + DynamoDB for state

## Content

| File | What's inside |
|------|---------------|
| `content/01-server-patterns.xml` | ConnectionManager, subscribe/broadcast, Redis Pub/Sub scale-out |
| `content/02-client-patterns.xml` | TypeScript client: reconnect with jitter, message queue, subscribe/unsubscribe lifecycle |

## Templates

| File | Purpose |
|------|---------|
| `templates/connection_manager.py` | FastAPI ConnectionManager with channel subscriptions and graceful disconnect |
| `templates/ws_client.ts` | TypeScript WebSocketClient: reconnect with exponential jitter, offline queue |

## Scripts

none
