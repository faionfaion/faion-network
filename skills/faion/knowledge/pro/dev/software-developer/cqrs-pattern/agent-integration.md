# Agent Integration — CQRS Pattern (software-developer)

## When to use
- Read-heavy domains where the read query shape diverges from the aggregate (dashboards, search, analytics) and JOINs in the write model are out of control.
- Front-end of an event-sourced system — queries hit projections, commands append events. CQRS + ES is the canonical pairing.
- Hard audit / regulatory domains (finance, healthcare, supply chain) where every state transition must be a named, immutable command.
- Multi-tenant SaaS where read replicas / per-tenant denormalized caches must scale independently of the write path.
- Step-up from CRUD when business behaviors (`PlaceOrder`, `ApproveLoan`, `CancelSubscription`) are getting buried in REST handlers.
- Microservices that publish domain events and need polyglot read stores (Postgres write, Elastic / Redis / OpenSearch read).

## When NOT to use
- Simple CRUD apps with <10 entities and roughly symmetric read/write loads — CQRS doubles surface area for zero benefit.
- Strong-consistency UX where the user must see their own write immediately and projections can't be made synchronous (most line-of-business forms with redirect-to-detail).
- Early-stage MVP / pre-PMF — the cost of write+read schemas, projections, and a bus is paid up-front but the domain isn't stable enough to justify it.
- Teams without DDD / event-driven experience — CQRS without aggregate boundaries degrades into "two layers of DTOs" with no payoff.
- Real-time collaborative editing where last-writer-wins on a single mutable doc is the right model (CRDT, OT — not CQRS).
- Tiny solo projects — the mediator/bus/projection plumbing is more code than the feature.

## Where it fails / limitations
- **Eventual-consistency UX leaks.** User places an order, navigates to "My Orders", doesn't see it. Without a read-your-writes strategy (sticky session on write store, optimistic UI, command-side return of projected DTO) you ship bug reports indistinguishable from data loss.
- **Projection drift.** Read store gets out of sync with events because of a deploy-without-rebuild, swallowed exception in the projector, or schema change. There must be a deterministic "rebuild from event log" command, otherwise corrupt reads ship.
- **Cross-aggregate queries.** When a query needs data from 3 aggregates with no read model for that combo, teams either (a) build a 4th projection, (b) JOIN in the API layer (slow), or (c) call multiple services (chatty). All three are visible regressions vs. a single SQL query in CRUD.
- **Command idempotency is not in the README sample.** Replays, retries, at-least-once buses cause double-charges if `command_id` isn't the dedup key. Real impl needs an `idempotency_key` table or saga state.
- **Bus-as-magic.** Mediator pattern hides handler resolution; "no handler found" + slow chain debugging across DI containers is painful. Static handler registries beat runtime discovery for agent-readability.
- **Versioned events.** Once projections exist, event payloads can't change freely; need event versioning + upcasting. Most teams discover this the first time they want to add a field.
- **Saga creep.** Multi-aggregate workflows (Place → Charge → Reserve → Ship) are NOT CQRS — they're sagas/process managers. Teams shoehorn sagas into command handlers; the model collapses.

## Agentic workflow
Drive CQRS scaffolding as a four-stage pipeline: (1) a design agent extracts the aggregate + command/query inventory from the spec; (2) a code-gen agent emits Command, CommandHandler, Query, QueryHandler, and Projection skeletons aligned to the repo's existing module structure (Python `cosmos`-style or .NET MediatR); (3) a test agent generates property-based tests for command idempotency and projection eventual consistency; (4) a review agent runs the anti-pattern checklist (commands returning data, queries with side effects, projections with business logic). Persist the inventory in `.aidocs/product_docs/cqrs-inventory.md` so subsequent feature work appends to it rather than forking a new model. Use `faion-sdd-executor-agent` to drive each command/query as one SDD task with handler + test + projection update as one unit.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — opus model fits because handler / projection trade-offs are non-trivial and easy to get wrong.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — run before committing event payloads / fixtures; commands often carry PII (`shipping_address`, `customer_id`, `payment_token`) that must not leak into test snapshots.
- A purpose-built **cqrs-review-agent** (worth adding under `agents/`): linter that greps handler files for the four canonical anti-patterns (command return type ≠ `None|UUID`, query handler with `await *.save(`, projection importing domain services, event without `occurred_at`).
- `faion-feature-executor` skill — sequential execution mode is correct for CQRS feature slices: command before query before projection before integration test; out-of-order task execution corrupts the read model.
- For event-sourced variants, pair with sibling `pro/dev/software-developer/event-sourcing/` — same agent set, additional snapshot/replay concerns.

### Prompt pattern
Inventory pass:
```
You are a CQRS architect. Given the feature spec in <spec>, produce a
table of Commands and Queries. Columns: name, intent, returns
(None/UUID for commands; DTO shape for queries), aggregate touched,
events emitted (commands only), read store index used (queries only).
Reject any command that returns a DTO. Reject any query that emits
events. Output as the markdown tables in cqrs-pattern/templates.md.
```

Anti-pattern review:
```
You are reviewing a PR adding CQRS handlers. Flag any of:
(1) command handler with return type other than None or UUID,
(2) query handler that calls *.save / *.update / publish_event,
(3) projection that imports from domain.<aggregate>.services,
(4) event class without occurred_at and aggregate_id,
(5) handler registered both as command AND query handler.
Cite file:line. Do not propose fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cosmos` (Python) | CQRS+ES reference framework from "Architecture Patterns with Python" | https://github.com/cosmicpython/code |
| `eventsourcing` (Python lib) | Aggregate, repository, event store, projection tooling | `pip install eventsourcing` ; https://eventsourcing.readthedocs.io |
| `MediatR` / `Mediator` (.NET) | Reference command/query mediator (MediatR commercial >$1M; Mediator is free source-gen) | `dotnet add package MediatR` ; https://github.com/martinothamar/Mediator |
| `axon-cli` | Axon Framework / Server inspector for JVM CQRS+ES | https://docs.axoniq.io |
| `eventstoredb` CLI | Append/read events, manage projections, replay | `brew install eventstore` ; https://www.eventstore.com/eventstoredb |
| `nats` CLI + JetStream | Lightweight command/event bus | `brew install nats-io/nats-tools/nats` ; https://nats.io |
| `dbt` | Build read-side projections as SQL models from append-only event/CDC table | https://docs.getdbt.com |
| `kafka-console-consumer` / `kcat` | Inspect events flowing into projections, replay from offset | https://github.com/edenhill/kcat |
| `Debezium` / `pgsync` | CDC from write store → read store when projector can't be added to legacy code | https://debezium.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| EventStoreDB | OSS + cloud | yes | Purpose-built event store; HTTP+gRPC APIs. Best fit for CQRS+ES. |
| Axon Server | Commercial + free dev tier | yes | Command/event/query bus + event store for JVM. |
| Marten (Postgres) | OSS | yes | CQRS+ES on Postgres — single-DB simplicity, good for solo/small team. |
| Apache Kafka + ksqlDB | OSS / Confluent SaaS | yes | Event log + streaming projections; overkill for <1k events/s. |
| NATS JetStream | OSS / Synadia SaaS | yes | Subjects = command/event topics. |
| Redis Streams | OSS | yes | Cheapest projection trigger; XADD on commit. |
| AWS EventBridge + DynamoDB Streams | SaaS | yes | Commands → Lambda → DDB → Stream → projector Lambda. |
| Temporal | OSS / Cloud | yes | Owns the saga / process-manager layer. CQRS handlers should NOT own this. |
| Apicurio / Confluent Schema Registry | SaaS / OSS | yes | Event schema versioning — non-optional once you have >1 projector. |
| Hasura / PostgREST | OSS | partially | Auto-generates a query-side API over read-model Postgres schema. |

## Templates & scripts

The methodology already ships handler/query/projection examples in `README.md` and templates in `templates.md`. Gap: automated lint of the four canonical anti-patterns. Inline drop-in (≤50 lines) — `scripts/cqrs-lint.sh`:

```bash
#!/usr/bin/env bash
# cqrs-lint.sh — flag CQRS anti-patterns in a Python codebase.
# Usage: cqrs-lint.sh <path-to-application-dir>
set -euo pipefail
root="${1:?usage: cqrs-lint.sh APPLICATION_DIR}"
fail=0
echo "# CQRS lint report ($root)"
echo "## Commands returning DTOs (must return None|UUID)"
grep -rEn 'class .*Handler\(CommandHandler' "$root" -A 6 \
  | grep -E 'def handle\(.*\) -> (?!None|UUID|None \| UUID)' \
  | tee /tmp/cqrs.cmd-ret || true
[[ -s /tmp/cqrs.cmd-ret ]] && fail=1
echo "## Query handlers with side effects"
grep -rEn 'class .*Handler\(QueryHandler' "$root" -A 30 \
  | grep -E 'await self\._.*\.(save|update|publish|delete)\(' \
  | tee /tmp/cqrs.qry-side || true
[[ -s /tmp/cqrs.qry-side ]] && fail=1
echo "## Projections importing domain services"
grep -rEn '^from domain\..*\.services' "$root/infrastructure/projections" 2>/dev/null \
  | tee /tmp/cqrs.proj-svc || true
[[ -s /tmp/cqrs.proj-svc ]] && fail=1
echo "## Events missing occurred_at or aggregate_id"
grep -rEn '^class .*Event' "$root/domain" -A 10 2>/dev/null \
  | awk '/^class .*Event/{name=$0; ok=0} /occurred_at/{ok++} /aggregate_id|order_id/{ok++} /^--$/{if(ok<2) print name; ok=0}' \
  | tee /tmp/cqrs.evt-fields || true
[[ -s /tmp/cqrs.evt-fields ]] && fail=1
exit "$fail"
```

Wire into `pre-commit`. Pair with the existing `templates.md` for command/query stubs and the README's mediator example for runtime wiring.

## Best practices
- **Handler = one transaction.** A command handler opens one unit of work, mutates one aggregate, emits its events, commits. Two aggregates = saga, not a fatter handler.
- **Stable command IDs from the client.** Client generates `command_id` (UUIDv7) and the handler dedups on it. Solves at-least-once retries cleanly.
- **Projections are passive and rebuildable.** No business rules, no service calls — only `read event → upsert read row`. Keep a `replay_projection(name, from_position=0)` admin command. If you can't rebuild, you don't have CQRS, you have two databases that lie about each other.
- **Read-your-writes via DTO return.** API layer (not the handler) optionally projects the just-committed aggregate to a DTO synchronously and returns it, while async projector still runs. Avoids the eventual-consistency UX trap without breaking the rule that handlers return `None|UUID`.
- **One read model per query, not per aggregate.** "OrderListByCustomer" and "OrderListByWarehouse" are two projections; do not share. Storage is cheap, JOINs at read time are not.
- **Event payloads are public API.** Once a projector or external consumer is on an event, you can't rename a field. Use additive evolution + upcasters; never edit a published event class.
- **Mediator should be a dict, not a framework.** Static `{CommandType: Handler}` registration in one composition root beats DI auto-discovery for agent-readability and grep-ability.
- **Test the projection contract, not the projector code.** Event log → expected read-store rows; catches schema drift across deploys far better than unit tests on the projection class.
- **Cap query DTO size.** Pagination + projection narrowing — never let a query handler return a list >page_size; agents will write `limit=10000` and OOM the read store.

## AI-agent gotchas
- **Agents collapse C and Q.** Asked to "implement get-or-create-order", the LLM produces a single handler that returns the entity. Constrain with structured output: `kind: command|query`, `returns_data: bool` — and reject mixed.
- **Hallucinated mediator APIs.** Agents invent `mediator.dispatch(...)`, `bus.fire(...)`, `mediator.execute(...)`. Pin the API in the prompt: "Use exactly `mediator.send(command)` for commands and `mediator.query(query)` for queries — see README §Command/Query Bus."
- **Projection forgets idempotency.** Agents write `await read_store.set(...)` without checking event order or `last_processed_position`. Replays then overwrite newer state with older. Force `position` check or UPSERT keyed on `(aggregate_id, event_position)`.
- **Read-side queries grow into reports.** Agents accept `GetSalesByRegionLastQuarter` and shove it into a query handler. That's analytics — route to a warehouse / dbt model, not the OLTP read store.
- **Event payload bloat.** Agents copy aggregate state into events (`OrderPlaced` with full Order JSON). Events should carry intent + minimal facts; reject events that look like CRUD snapshots.
- **No saga awareness.** Multi-step business flows tempt agents to build a fat command handler that calls 4 services. Force a hand-off: anything past one aggregate goes to a process manager / Temporal workflow.
- **Tests over-stub the bus.** Agents mock the mediator and test the handler in isolation, missing serialization/registration bugs. Require ≥1 end-to-end test per feature where command goes through the real bus and query reads the real projection.
- **Human-in-the-loop on event versioning.** When the agent proposes adding/removing an event field, stop. Schema changes need the human to decide upcaster vs. new event vs. backfill. Never auto-merge event-class changes.
- **Auto-fan-out to too many projections.** Agents enthusiastically add a new projection per query. Cap at N projections per aggregate (e.g., 3) and force review before adding the 4th — usually the right fix is a wider existing projection or an analytics layer.

## References
- Fowler, M. "CQRS." https://martinfowler.com/bliki/CQRS.html
- Microsoft Architecture Patterns — CQRS. https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs
- Young, G. "CQRS Documents." https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf
- Vernon, V. "Implementing Domain-Driven Design," ch. 4, 8.
- Percival, H. & Gregory, B. "Architecture Patterns with Python," ch. 12. https://www.cosmicpython.com
- EventStoreDB docs — Projections. https://developers.eventstore.com/server/latest/projections.html
- Axon Reference Guide — CQRS architecture. https://docs.axoniq.io
- Marten — CQRS / event store on Postgres. https://martendb.io/events
- Sibling methodologies in this repo: `pro/dev/software-developer/event-sourcing/`, `pro/dev/code-quality/cqrs-pattern/`, `pro/dev/code-quality/event-sourcing-basics/`, `pro/dev/code-quality/domain-driven-design/`, `pro/dev/code-quality/clean-architecture/`.
