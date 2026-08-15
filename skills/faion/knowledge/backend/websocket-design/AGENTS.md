# WebSocket Design

## Summary

**One-sentence:** Designs a WebSocket service with versioned envelope, heartbeat/ping-pong, exponential reconnect with full jitter, Redis Pub/Sub fan-out, and bounded backpressure queues.

**One-paragraph:** Designs a WebSocket service with versioned envelope, heartbeat/ping-pong, exponential reconnect with full jitter, Redis Pub/Sub fan-out, and bounded backpressure queues. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Server-pushed events at sub-second latency (chat, presence, live cursors, multiplayer state).
- Bidirectional stream where the client also sends frequently (collaborative editing, voice control loops).
- Horizontal scaling requirement: multiple worker processes serving a single channel.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Server-pushed events at sub-second latency (chat, presence, live cursors, multiplayer state).
- Bidirectional stream where the client also sends frequently (collaborative editing, voice control loops).
- Horizontal scaling requirement: multiple worker processes serving a single channel.

## Skip If (ANY kills it)

- One-shot CRUD or rare polls every >5 seconds — REST is cheaper.
- Server-only push with no client→server traffic — SSE wins on simplicity + HTTP/2 multiplexing + resume.
- Pure serverless (Lambda) tier without API Gateway WebSocket adapter.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Message catalog | shared schema (Zod/Pydantic/protobuf) | team |
| Auth ticket source | POST /ws-ticket endpoint | auth team |
| PubSub bus | Redis or NATS | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-rest-design]] | ticket endpoint and lifecycle webhooks ride on top of REST conventions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 testable rules (envelope, heartbeat, per-type schema, close codes, jitter, fan-out, bounded queue, short-lived token, skip) | 1700 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden patterns | 1200 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns with symptom + root-cause + fix | 1400 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure incl. per-type schemas, shed policy and token TTL | 1300 |
| `content/05-examples.xml` | reference | Two full worked examples end-to-end with the trace and the resulting artefact | 1200 |
| `content/06-decision-tree.xml` | essential | Protocol-choice tree + 8 protocol-hygiene gates → conclusion(ref=rule-id); skip leaf always reachable | 1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `envelope-design` | sonnet | Schema design with versioning + dedup is medium-judgement work. |
| `reconnect-implementation` | sonnet | Mechanical exponential backoff + jitter. |
| `backpressure-audit` | haiku | Grep for unbounded queues + missing rate limits. |

## Templates

| File | Purpose |
|------|---------|
| `templates/connection_manager.py` | FastAPI ConnectionManager: channel subscriptions, presence map, graceful disconnect with truthful close codes |
| `templates/envelope.schema.json` | JSON Schema for the envelope plus one example message type |
| `templates/ws_client.ts` | TypeScript WebSocketClient: reconnect with exponential jitter, offline queue, heartbeat |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-websocket-design.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[api-rest-design]]
- [[api-authentication]]
- [[api-rate-limiting]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Does the workload require sub-second server push AND client→server traffic?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/connection_manager.py`

```python
import asyncio
import logging

from fastapi import WebSocket
from fastapi.websockets import WebSocketState

# RFC 6455 close codes this manager emits (rule close-code-truthful).
CLOSE_NORMAL = 1000
CLOSE_GOING_AWAY = 1001
CLOSE_POLICY_VIOLATION = 1008


class ConnectionManager:
    """Per-process. Cross-node fan-out belongs on Redis Pub/Sub, not here."""

    def __init__(self) -> None:
        self.connections: dict[str, WebSocket] = {}          # user_id -> socket
        self.subscribers: dict[str, set[str]] = {}           # channel -> user_ids
        self.user_channels: dict[str, set[str]] = {}         # user_id -> channels

    async def connect(self, user_id: str, ws: WebSocket) -> None:
        await ws.accept()
        if user_id in self.connections:
            await self.disconnect(user_id, code=CLOSE_GOING_AWAY)
        self.connections[user_id] = ws
        self.user_channels[user_id] = set()
        logging.info("ws connect user=%s", user_id)

    async def disconnect(self, user_id: str, code: int = CLOSE_NORMAL) -> None:
        for channel in list(self.user_channels.get(user_id, ())):
            self.unsubscribe(user_id, channel)
        ws = self.connections.pop(user_id, None)
        self.user_channels.pop(user_id, None)
        if ws and ws.client_state == WebSocketState.CONNECTED:
            await ws.close(code=code)
        logging.info("ws disconnect user=%s code=%s", user_id, code)

    def subscribe(self, user_id: str, channel: str) -> None:
        self.subscribers.setdefault(channel, set()).add(user_id)
        self.user_channels.setdefault(user_id, set()).add(channel)

    def unsubscribe(self, user_id: str, channel: str) -> None:
        subs = self.subscribers.get(channel)
        if subs:
            subs.discard(user_id)
            if not subs:
                del self.subscribers[channel]
        self.user_channels.get(user_id, set()).discard(channel)

    async def send_to_user(self, user_id: str, envelope: dict) -> None:
        ws = self.connections.get(user_id)
        if not ws or ws.client_state != WebSocketState.CONNECTED:
            return
        try:
            await ws.send_json(envelope)
        except Exception as exc:  # noqa: BLE001 — a dead socket must not kill the loop
            logging.error("ws send failed user=%s: %s", user_id, exc)
            await self.disconnect(user_id, code=CLOSE_POLICY_VIOLATION)

    async def broadcast(self, channel: str, envelope: dict) -> None:
        targets = list(self.subscribers.get(channel, ()))
        await asyncio.gather(
            *(self.send_to_user(uid, envelope) for uid in targets),
            return_exceptions=True,
        )
```

### `templates/envelope.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/ws-envelope.json",
  "title": "envelope",
  "type": "object",
  "required": [
    "v",
    "type",
    "channel",
    "id",
    "seq",
    "ts",
    "payload"
  ],
  "additionalProperties": false,
  "properties": {
    "v": {
      "type": "integer",
      "enum": [
        1
      ]
    },
    "type": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9]*(\\.[a-z][a-z0-9]*)+$"
    },
    "channel": {
      "type": "string",
      "minLength": 1
    },
    "id": {
      "type": "string",
      "description": "Per-message idempotency key for retries."
    },
    "seq": {
      "type": "integer",
      "minimum": 0,
      "description": "Monotonic per-channel; clients dedupe on it across reconnects."
    },
    "ts": {
      "type": "integer",
      "description": "Unix milliseconds at send time."
    },
    "payload": {
      "type": "object"
    }
  },
  "$defs": {
    "chat.message": {
      "type": "object",
      "required": [
        "text",
        "from"
      ],
      "properties": {
        "text": {
          "type": "string",
          "maxLength": 4000
        },
        "from": {
          "type": "string"
        }
      }
    }
  }
}
```

### `templates/ws_client.ts`

```typescript
// faion_header_json: {"__faion_header__":{"purpose":"TypeScript WebSocketClient: reconnect with exponential jitter, offline queue, heartbeat","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#versioned-envelope","token_budget_impact":"~150 tokens when loaded"}}
type Msg = { v: number; type: string; channel: string; seq: number; ts: number; payload: unknown };

export class WSClient {
  private ws?: WebSocket;
  private attempts = 0;
  private queue: Msg[] = [];
  private readonly maxQueue = 100;
  private readonly url: string;
  private heartbeat?: ReturnType<typeof setInterval>;

  constructor(url: string) { this.url = url; this.connect(); }

  private connect() {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => { this.attempts = 0; this.flush(); this.startHeartbeat(); };
    this.ws.onclose = () => { this.stopHeartbeat(); this.scheduleReconnect(); };
    this.ws.onmessage = (e) => this.handle(JSON.parse(e.data));
  }

  private scheduleReconnect() {
    if (this.attempts > 8) return;
    const cap = 30_000, base = 1000;
    const delay = Math.random() * Math.min(cap, base * Math.pow(2, this.attempts));
    this.attempts += 1;
    setTimeout(() => this.connect(), delay);
  }

  private startHeartbeat() { this.heartbeat = setInterval(() => this.send({ type: 'ping' } as Msg), 25_000); }
  private stopHeartbeat() { if (this.heartbeat) clearInterval(this.heartbeat); }
  private flush() { while (this.queue.length && this.ws?.readyState === 1) this.ws.send(JSON.stringify(this.queue.shift())); }
  private handle(_m: Msg) { /* delegate to listeners */ }
  send(m: Msg) {
    if (this.queue.length >= this.maxQueue) this.queue.shift();
    this.queue.push(m); this.flush();
  }
}
```
