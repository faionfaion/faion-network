# WebSocket Design

## Summary

WebSocket provides full-duplex, persistent connections between clients and servers. Core rule: authenticate on the upgrade handshake before accepting the connection, implement heartbeats below the load-balancer idle timeout, and reconnect with exponential backoff plus jitter on the client side.

## Why

Polling for frequently changing data wastes requests and adds latency. WebSockets enable server-push with sub-100ms delivery. Without heartbeats, stale connections consume file descriptors indefinitely. Without reconnect backoff, a server restart triggers a reconnect storm that DDoSes your own service.

## When To Use

- Real-time UI features: chat, presence indicators, live cursors, notification feeds
- Server-pushed updates where polling burns requests (price tickers, game state, dashboards)
- Bidirectional protocols (collaborative editing, low-latency RPC) where SSE alone is insufficient
- Frontends needing one persistent connection multiplexed across many topics per user

## When NOT To Use

- One-way server-to-client streams — use Server-Sent Events; simpler, works through more proxies
- Request/response-style RPC — use HTTP/gRPC; WebSockets add framing overhead and connection state
- Behind aggressive corporate proxies that strip WebSocket upgrades — fall back to long-polling
- Serverless platforms without WS support — use AWS API Gateway WebSockets or Cloudflare Durable Objects

## Content

| File | What's inside |
|------|---------------|
| `content/01-connection-manager.xml` | Server-side connect/disconnect/subscribe/broadcast patterns; channel management |
| `content/02-client-patterns.xml` | TypeScript client with reconnect, exponential backoff, message queue, heartbeat |
| `content/03-scaling.xml` | Redis pub/sub fan-out for multi-instance deployments; cross-node broadcast |
| `content/04-antipatterns.xml` | No heartbeat, unbounded connections, missing auth, no reconnect logic, blocking handlers |

## Templates

| File | Purpose |
|------|---------|
| `templates/connection-manager.py` | FastAPI ConnectionManager with channel subscriptions and broadcast |
| `templates/ws-client.ts` | TypeScript WebSocketClient with reconnect, queue, and heartbeat |
