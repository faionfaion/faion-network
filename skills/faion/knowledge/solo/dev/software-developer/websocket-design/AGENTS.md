---
slug: websocket-design
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: WebSocket protocol spec: typed message envelope with version + id, heartbeat ping/pong with TTL, exponential reconnect with jitter, backpressure on send queue, auth via short-lived token, JSON-schema validation per message type.
content_id: "355a37e23b03d132"
complexity: medium
produces: spec
est_tokens: 5000
tags: [websocket, realtime, heartbeat, reconnect, backpressure]
---
# WebSocket Design

## Summary

**One-sentence:** WebSocket protocol spec: typed message envelope with version + id, heartbeat ping/pong with TTL, exponential reconnect with jitter, backpressure on send queue, auth via short-lived token, JSON-schema validation per message type.

**One-paragraph:** WebSocket connections rot when the message envelope is freeform JSON (clients break on field drift), when there is no heartbeat (NAT dies silently), when reconnect logic hammers the server on outage, when the send queue is unbounded (server OOMs), and when auth is via long-lived cookies (token theft is permanent). This methodology produces a spec: versioned envelope `{v, type, id, ts, payload}`, ping/pong every 30s with TTL, exponential reconnect with full jitter, bounded outgoing queue with shed policy, short-lived (5min) signed token at handshake, JSON schema per message type validated on both sides.

**Ефективно для:**

- Перший WebSocket сервіс - зафіксувати envelope + heartbeat + reconnect.
- Connections silently die після 30 хв - впровадити ping/pong.
- Reconnect storm після збою - exponential backoff + jitter.
- Server OOM від unbounded send queue - bounded + shed policy.
- Auth через cookie - short-lived signed token.

## Applies If (ALL must hold)

- Service uses WebSocket (RFC 6455) for bidirectional real-time messaging.
- Connections are long-lived (>30s) and pass through NAT / corporate firewalls.
- Server has finite memory and accepts many concurrent connections.
- Auth model permits short-lived tokens.

## Skip If (ANY kills it)

- Use case is one-shot SSE (Server-Sent Events) - use SSE methodology.
- Use case is pure REST polling - WebSocket overhead is not justified.
- Tiny demo with <10 concurrent connections.
- Protocol is gRPC bi-directional streaming - use gRPC methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Message taxonomy | list of message types + JSON schema per type | engineering |
| Auth model | short-lived token signing | security |
| Reconnect policy | expected outage window | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rate-limiting]] | WS connections share rate-limit budget with REST API. |
| [[rust-tokio-async]] | common async runtime hosting the WS server. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: versioned envelope, heartbeat 30s, reconnect with jitter, bounded send queue, short-lived token, schema per type, close codes | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: envelope, heartbeat, reconnect, send queue, auth + schemas | ~900 |
| `content/05-examples.xml` | essential | Worked example for a multiplayer chat WS service | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-envelope` | sonnet | Per-message-type judgement. |
| `wire-heartbeat` | haiku | Boilerplate setInterval. |
| `reconnect-client` | sonnet | Backoff math + edge cases (token expiry mid-reconnect). |
| `size-send-queue` | opus | Stakes high; wrong shed policy drops user data. |

## Templates

| File | Purpose |
|------|---------|
| `templates/envelope.schema.json` | JSON Schema for the WS envelope + 1 example message type. |
| `templates/client.ts` | Client reconnect + heartbeat skeleton with exponential backoff + full jitter. |
| `templates/connection-manager.py` | Python connection-manager: presence map + heartbeat + room broadcast. |
| `templates/ws-client.ts` | TS WebSocket client wrapper: backoff reconnect + heartbeat + envelope. |
| `templates/_smoke-test.json` | Minimum viable WS spec for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-websocket-design.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[rate-limiting]]
- [[rust-tokio-async]]
- [[api-error-handling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - envelope shape, heartbeat presence, reconnect logic, queue boundedness - onto a rule from `content/01-core-rules.xml`. Use it before merging WS code: it catches no-heartbeat and reconnect-storm upstream.
