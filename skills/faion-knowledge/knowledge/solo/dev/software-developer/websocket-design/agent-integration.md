# Agent Integration — WebSocket Design

## When to use
- Real-time UI features: chat, presence, live cursors, notifications, dashboards.
- Server-pushed updates where polling would burn requests (price tickers, game state).
- Bidirectional protocols (collaborative editing, low-latency RPC) where SSE alone is insufficient.
- Frontends that need persistent connection multiplexed across many topics/channels per user.

## When NOT to use
- One-way server → client streams — use Server-Sent Events (SSE); HTTP/1.1 + reconnect for free, works through more proxies.
- Request/response style RPC — use HTTP/gRPC; WebSockets add framing overhead and connection-state burden.
- Behind aggressive corporate proxies that strip WebSocket upgrades — fall back to long-polling (Socket.IO does this).
- Serverless platforms without WS support (some FaaS) — use AWS API Gateway WebSockets, Cloudflare Durable Objects, Ably, or Pusher instead.

## Where it fails / limitations
- Stateful: every connection consumes a file descriptor + memory; ~10k connections per process is the typical Linux ceiling without tuning (`nofile`, `tcp_mem`).
- Sticky sessions required across multi-instance deployments unless you fan out via Redis/NATS pub/sub.
- Network instability: mobile clients disconnect constantly; reconnect storms after a deploy can DoS your own service.
- No HTTP cache; every consumer reconnect re-fetches initial state.
- Authentication: subprotocols vary (Bearer in `Sec-WebSocket-Protocol`, query string token, cookie). Each has tradeoffs.
- Backpressure: a slow client can block the producer; without bounded queues, server memory grows unbounded.
- Heartbeat tuning is per-network: 30s pings break behind some load balancers (AWS ALB idle timeout default is 60s — reduce to 25s to keep alive).
- Message ordering is per-connection only; cross-instance fan-out via pub/sub provides no ordering guarantee.

## Agentic workflow
Drive WebSocket work in three layers: (1) protocol design (message envelope: `type`, `channel`, `data`, `id`, `ts` — versioned), (2) server connection-manager (connect/disconnect/subscribe/broadcast), (3) client with reconnect + queue + heartbeat. Use a subagent to enforce the message-envelope schema with TypeScript/Pydantic models on both sides, regenerated from a single source. Always implement an auth handshake on `connect` before subscribing — never accept anonymous upgrades and authorize later.

### Recommended subagents
- `ws-protocol-architect` (Sonnet) — defines message envelope, channel naming, versioning.
- `ws-server-implementer` (Sonnet) — writes the connection manager, channel manager, distributed pub/sub adapter.
- `ws-client-implementer` (Sonnet) — writes the client with reconnect, queue, heartbeat, subscribe/unsubscribe lifecycle.
- `ws-loadtester` (Sonnet) — runs `k6` or `artillery` ws scenarios, measures p95 latency at N connections.
- `ws-security-reviewer` (Sonnet) — checks auth handshake, origin validation, rate limits, message-size cap.

### Prompt pattern
```
Task: add presence channel to existing WS service.
Schema (Pydantic + zod):
- PresenceJoin { userId, room, status: 'online'|'away'|'busy' }
- PresenceUpdate { userId, status }
- PresenceLeave { userId }
Server:
- on subscribe to "presence:<room>": broadcast current member list.
- on disconnect: emit PresenceLeave to room.
Client:
- batch presence updates over 250 ms before re-rendering.
Backpressure: drop messages older than 5s if client queue > 100.
Done = stress test 1k clients × 5 rooms, p95 broadcast < 100 ms, zero leaked goroutines/tasks after disconnect.
```

```
Audit: WebSocket security checklist.
Verify on /ws endpoint:
- Origin header validation against allowlist.
- Auth before accept (token in subprotocol or query, validated with short-lived JWT).
- Per-connection rate limit (e.g., 50 msg/sec).
- Max message size enforced (ws library option).
- TLS only (wss://); reject ws:// in production config.
Output: pass/fail per check + patch.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `wscat` | CLI WebSocket client for testing | `npm i -g wscat` |
| `websocat` | Rust-built ws CLI, scripting-friendly | https://github.com/vi/websocat |
| `k6` | Load testing with `k6/ws` module | https://k6.io |
| `artillery` | Load testing with WS plugin | `npm i -g artillery` |
| `wireshark` / `tshark` | Wire-level frame inspection | https://wireshark.org |
| Browser DevTools → Network → WS | Frame inspector | Built-in |
| `socket.io-cli` | Test Socket.IO endpoints | `npm i -g socket.io-client-tool` |
| `nchan` (nginx module) | Pub/sub broker over HTTP+WS | https://nchan.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Ably | SaaS | Yes via REST + SDK | Managed pub/sub, presence, history; 99.999% SLA |
| Pusher Channels | SaaS | Yes via REST | Long-standing; client SDKs everywhere |
| Soketi | OSS | Yes | Pusher-compatible, self-hosted |
| Centrifugo | OSS | Yes via API | Go server, Redis/ Nats engine, GRPC API |
| Cloudflare Durable Objects | SaaS | Yes via API | Edge WebSockets with built-in state |
| AWS API Gateway WebSockets | SaaS | Yes via REST | Serverless WS; Lambda handlers per route |
| Phoenix Channels (Elixir) | OSS | Yes | High-throughput, BEAM-native |
| Socket.IO | OSS lib | Yes | Adds polling fallback; node + many ports |
| NATS / Redis Streams + ws gateway | OSS | Yes | Common DIY backend for cross-node fan-out |
| Liveblocks | SaaS | Yes via SDK | Collaborative cursors / multiplayer presence |

## Templates & scripts
See `templates.md`. Useful k6 stress test (≤50 lines):

```js
// k6 run --vus 1000 --duration 60s ws-stress.js
import ws from 'k6/ws';
import { check } from 'k6';
import { Trend } from 'k6/metrics';

const broadcastLatency = new Trend('ws_broadcast_ms');

export default function () {
  const url = 'wss://api.example.com/ws/' + __VU;
  const room = `chat:room-${__VU % 10}`;
  ws.connect(url, {}, (socket) => {
    socket.on('open', () => {
      socket.send(JSON.stringify({ type: 'subscribe', channel: room }));
      const sentAt = Date.now();
      socket.send(JSON.stringify({ type: 'message', channel: room, data: { sentAt } }));
    });
    socket.on('message', (raw) => {
      const m = JSON.parse(raw);
      if (m.type === 'message' && m.data?.sentAt) {
        broadcastLatency.add(Date.now() - m.data.sentAt);
      }
    });
    socket.setTimeout(() => socket.close(), 30000);
  });
  check(null, { 'no error': () => true });
}
```

## Best practices
- Authenticate on the upgrade handshake, not after — pass a short-lived JWT in `Sec-WebSocket-Protocol` (more proxy-friendly than query strings) or in a cookie set by a recent HTTP login.
- Validate `Origin` server-side against an allowlist; same-origin is not enforced for WebSockets.
- Use a typed message envelope versioned via `v` field (`{ v: 1, type, channel, ... }`) so clients/server can negotiate.
- Heartbeats: set ping interval below load-balancer idle timeout; close connection if no pong in 2× interval.
- Implement per-connection bounded queues; drop or close on overflow rather than buffering unbounded.
- Cap message size (e.g., 64 KB) at the framework level (FastAPI, Starlette, ws lib option).
- For multi-instance deployment, use Redis/NATS pub/sub fan-out and trace cross-instance latency.
- Reconnect with exponential backoff + jitter on the client; never reconnect immediately on close.
- Buffer outgoing messages on the client during disconnect; flush on reconnect (with idempotency keys).
- Keep recent history (last N messages) on the server, sent on subscribe/reconnect to fill gaps.
- Apply rate limits per connection (msg/sec) and per user across connections.
- Log every connect/disconnect with reason code + duration; alarms on disconnect-rate spikes.

## AI-agent gotchas
- The README's example connection manager has a subtle bug: `disconnect` while inside `connect()`'s try block races; agents replicate this pattern. Require a redesign that doesn't call `disconnect` during `accept`.
- Agents leave `print`/`logging.error` instead of structured logging — every WS error needs `connection_id`, `user_id`, `channel`, `code`.
- Forgotten cleanup: subscribers map keeps stale `user_id`s after disconnect — verify membership cleanup with a goroutine/task count test.
- Agents enable broadcast across instances by adding Redis pub/sub but forget to skip self-publish — leads to message dupes.
- Reconnect storms after deploy: agents copy "reconnect immediately" code; require backoff + jitter with `Math.random()`.
- Forgetting `ctx.client_state == CONNECTED` check before send — raises on a closed socket.
- Agents broadcast unbounded objects (`data: <huge json>`) — enforce envelope size cap server-side.
- Subscriptions leaking across user sessions: agents key state by socket but reuse user_id across reconnects without revoking old subscriptions.
- Authorization on subscribe is forgotten — agents allow any client to subscribe to any channel including admin channels.
- Human-in-loop checkpoint: any new channel/message type that crosses tenancy boundaries (cross-user broadcast, admin events) needs human review of the auth path.

## References
- https://datatracker.ietf.org/doc/html/rfc6455 (WebSocket Protocol)
- https://datatracker.ietf.org/doc/html/rfc8441 (HTTP/2 WebSocket)
- https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- https://fastapi.tiangolo.com/advanced/websockets/
- https://socket.io/docs/v4/
- https://centrifugal.dev
- https://ably.com/topic/websockets (overview, scaling guide)
- https://www.cloudflare.com/learning/serverless/glossary/websocket/
- https://lucumr.pocoo.org/2020/4/14/websockets/ (Armin Ronacher on WS pitfalls)
- https://k6.io/docs/using-k6/protocols/websockets/
