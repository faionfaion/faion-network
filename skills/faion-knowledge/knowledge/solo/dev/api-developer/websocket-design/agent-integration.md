# Agent Integration — WebSocket Design

## When to use
- Server-pushed events at sub-second latency: chat, presence, live cursors, order book updates, multiplayer state.
- Bidirectional streams where the client also sends frequently (collab editing, voice control loops).
- High-frequency updates where polling would burn 10x bandwidth.
- LLM streaming when SSE is not enough (binary frames, two-way tool calls). Otherwise prefer SSE — simpler, proxy-friendly.
- Agent pipelines that need a long-lived control channel (workers reporting progress to a dashboard).

## When NOT to use
- One-shot CRUD or rare polls (every >5s) — REST is cheaper.
- Server-only push, no client→server traffic — SSE wins on simplicity, HTTP/2 multiplexing, and resume.
- Behind misconfigured proxies / corporate firewalls that strip Upgrade headers — fall back to SSE or long-poll.
- Mobile networks with aggressive NAT timeouts unless you commit to heartbeats and resumption.
- When you cannot run a stateful tier — pure serverless (Lambda) supports WS only via API Gateway, with state in DynamoDB.

## Where it fails / limitations
- Stickiness: sockets are pinned to one process — naive horizontal scaling breaks fan-out without a pubsub bus.
- Backpressure is silent: a slow client fills the server's send buffer and the message loop blocks. Always cap with bounded queues + drop policy.
- Reconnect storms after a deploy can DoS your own auth endpoint. Stagger with jitter + cap exponential backoff.
- No native message ordering guarantees across reconnects; clients must dedupe by sequence ID.
- Auth on Upgrade is fiddly — browsers can't send custom headers. Use cookie auth or short-lived ticket in query string.
- Long-lived connections amplify memory leaks; restart bleeds users on every deploy unless you implement graceful drain.
- WebSocket frame size limits in proxies (nginx default 1MB) silently truncate or close; set `proxy_max_temp_file_size` etc.

## Where it fails / limitations (continued)
- Without rate limiting per connection, one bad client can consume an entire CPU.

## Agentic workflow
Treat the WS protocol as a typed contract: define the message envelope (type, channel, seq, payload) in shared schema (Zod / Pydantic / protobuf). Agents that add a new message type must update both server handler and client union, plus a contract test. For scale, push fan-out to Redis Pub/Sub or NATS so any worker can serve any client; the agent only writes per-process logic.

### Recommended subagents
- `faion-feature-executor` — drives ordered tasks: schema → server handler → client handler → reconnect test.
- `faion-sdd-execution` — quality gate enforcing heartbeat, auth, bounded queue, reconnect with jitter.
- A `protocol-reviewer` agent (Opus) — checks new message types for backward compatibility and missing ack/seq.
- `nero-tools` — when WS feeds into NERO pipelines, hooks for `tg-send` on backpressure events.

### Prompt pattern
```
Add a `presence` message type to ws/protocol.ts and ws/protocol.py.
Server: on receive, broadcast {type:"presence", userId, status, ts} to
channel `presence:<orgId>` via Redis Pub/Sub. Client: subscribe in
PresenceProvider.tsx, expose useUsersOnline() hook. Add a vitest that
spins two clients and asserts cross-broadcast within 200ms. No new deps.
```

```
Audit ConnectionManager.ts for backpressure handling. If send buffer is
unbounded or there is no drop/disconnect on slow consumer, propose a
patch using a 64-message bounded queue and disconnect-on-overflow.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `websocat` | curl for WS — connect, pipe stdin, debug | `cargo install websocat` or `brew install websocat` |
| `wscat` | Node-based WS client | `npm i -g wscat` |
| `autobahn-testsuite` | RFC 6455 conformance fuzz | `pip install autobahntestsuite` |
| `k6` | Load test WS connections + messages | k6.io/docs/using-k6/protocols/websockets |
| `artillery` | Scenario-based WS load testing | `npm i -g artillery` |
| `wrk2-ws` / `tsung` | Sustained-load WS testing | OSS |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Pusher Channels | SaaS | Yes — REST trigger API | Hosted WS broker, generous free tier |
| Ably | SaaS | Yes — REST + SDK | Realtime + history, message ordering guarantees |
| Soketi | OSS | Yes | Self-hosted Pusher-compatible drop-in |
| Centrifugo | OSS | Yes — HTTP API for publish | Go server, Redis/Nats engine, JWT auth |
| AWS API Gateway WebSocket | SaaS | Yes — IaC | Pairs with Lambda, state in DynamoDB |
| Cloudflare Durable Objects + WebSockets | SaaS | Yes — wrangler CLI | Stateful at edge; pricing per duration |
| Supabase Realtime | SaaS + OSS | Yes — postgres-driven | Postgres CDC over WS |
| LiveKit | OSS + SaaS | Yes — CLI + SDK | Built on WebRTC but WS for signaling |

## Templates & scripts
See `templates.md` and `examples.md` for FastAPI ConnectionManager, Redis pubsub, TS client.

Quick load + reconnect smoke (k6):

```javascript
// ws-smoke.js  →  k6 run --vus 200 --duration 60s ws-smoke.js
import ws from 'k6/ws';
import { check } from 'k6';

export default function () {
  const url = `wss://api.example.com/ws/${__VU}`;
  const res = ws.connect(url, { headers: { Cookie: __ENV.COOKIE } }, (socket) => {
    socket.on('open', () => {
      socket.send(JSON.stringify({ type: 'subscribe', channel: 'feed:global' }));
      socket.setInterval(() => socket.ping(), 25000);
    });
    socket.on('message', (m) => check(m, { 'has type': (x) => JSON.parse(x).type }));
    socket.setTimeout(() => socket.close(), 50000);
  });
  check(res, { 'status 101': (r) => r && r.status === 101 });
}
```

## Best practices
- Define a versioned message envelope: `{v, type, channel, seq, ts, payload}`. Bump `v` for breaking changes.
- Heartbeat: client pings every 25–30s, server disconnects after 2 missed. Inside any LB / NAT idle timeout.
- Exponential reconnect with full jitter (`min(cap, base*2^n) * random()`); cap retries to avoid storms.
- Auth on Upgrade: short-lived ticket from REST `/ws-ticket` exchanged for a session cookie. Don't ship JWTs in query strings to logs.
- Bounded send queue per connection (e.g. 64 messages). On overflow: drop, mark, or disconnect — never block the loop.
- Per-connection rate limit (msgs/sec) and per-user connection cap (3–5).
- Horizontal scale via pubsub fan-out (Redis, NATS, Kafka). Clients reconnect to any node, state is shared.
- Graceful drain on deploy: set `Connection: close`, broadcast `server-shutting-down`, wait for clients to reconnect to a healthy node.
- Compress only large payloads (`permessage-deflate`); for short, frequent messages it adds latency.
- Log: connect, disconnect (with reason code), backpressure drops, auth failures. Not every message.

## AI-agent gotchas
- LLM-generated WS code often forgets `await ws.close()` on errors → file descriptor leak. Inspect every disconnect path.
- "Helpful" agents reintroduce module-global state for connections, breaking horizontal scale. Force per-process plus pubsub.
- Heartbeat code is frequently dropped during refactors because tests still pass — wire a 60s integration test that asserts ping/pong.
- Reconnect logic without jitter looks fine in unit tests and self-DDoSes in prod after a deploy. Reject any reconnect PR without `jitter` or `random` in the diff.
- Subscription cleanup is invisible: an agent adding a new subscriber must also remove it on unmount/disconnect. Use a linter rule that requires paired `subscribe/unsubscribe`.
- Agents debugging WS issues may try to "just reconnect" rather than diagnose. Surface disconnect reason codes (1006, 1011, 4xxx) in logs and require the agent to cite the code before patching.
- For LLM streaming over WS, agents may forget to send a terminal frame, leaving clients spinning. Always send a `done` frame and a close code; test the cancel path.
- Cloudflare/nginx default idle timeouts (100s) silently drop connections. Document the proxy config alongside the server code so the agent does not "fix" the symptom in app code.

## References
- https://datatracker.ietf.org/doc/html/rfc6455
- https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- https://fastapi.tiangolo.com/advanced/websockets/
- https://redis.io/docs/manual/pubsub/
- https://centrifugal.dev/
- https://k6.io/docs/using-k6/protocols/websockets/
- https://www.ably.com/topic/websockets-vs-sse
- https://en.wikipedia.org/wiki/Thundering_herd_problem
