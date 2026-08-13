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
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `envelope-design` | sonnet | Schema design with versioning + dedup is medium-judgement work. |
| `reconnect-implementation` | sonnet | Mechanical exponential backoff + jitter. |
| `backpressure-audit` | haiku | Grep for unbounded queues + missing rate limits. |

## Templates

| File | Purpose |
|------|---------|
| `templates/connection_manager.py` | FastAPI ConnectionManager with channel subscriptions and graceful disconnect |
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
# faion_header_json: {"__faion_header__":{"purpose":"FastAPI ConnectionManager with channel subscriptions and graceful disconnect","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#versioned-envelope","token_budget_impact":"~150 tokens when loaded"}}
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = {}

    async def connect(self, channel: str, ws: WebSocket) -> None:
        await ws.accept()
        self.active.setdefault(channel, []).append(ws)

    async def disconnect(self, channel: str, ws: WebSocket) -> None:
        self.active.get(channel, []).remove(ws)

    async def broadcast(self, channel: str, message: dict) -> None:
        for ws in list(self.active.get(channel, [])):
            try:
                await ws.send_json(message)
            except Exception:
                self.active[channel].remove(ws)
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
