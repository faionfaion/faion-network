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
| `templates/_smoke-test.py` | Minimum viable filled-in artefact for sanity-checking the schema. |

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
