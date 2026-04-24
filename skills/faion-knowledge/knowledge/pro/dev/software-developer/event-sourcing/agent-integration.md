# Agent Integration — Event Sourcing

## When to use
- Domains where the audit trail IS the requirement (banking, ledger, healthcare records, compliance-heavy SaaS).
- Aggregates where temporal queries are needed: "what was the state on date X", "who changed Y when".
- Systems where business rules evolve and you need to replay history through new logic (recompute royalties, retry failed reconciliations).
- Front-end of a CQRS system with multiple read models that must stay in sync from one truth — events are that truth.
- Domain-event-driven microservices where downstream consumers (search, analytics, ML feature store) subscribe to a published event log.
- Workflows requiring undo / what-if analysis (engineering simulators, financial projections).

## When NOT to use
- CRUD-shaped data with no audit need — events double the storage and triple the complexity for no payoff.
- Reporting-first products where the dominant access pattern is aggregate analytics — keep a relational warehouse, not an event store.
- Strong real-time consistency UX (banking transfer that must instantly show the new balance to the same user) without a careful read-your-writes strategy.
- Tiny solo apps and pre-PMF MVPs — the event/projection plumbing dwarfs the feature.
- Teams without DDD experience — without aggregate boundaries, the event log degenerates into a CDC log of CRUD updates ("UserNameChanged", "UserNameChanged", "UserNameChanged").
- Domains where regulatory rules require destruction (GDPR right to erasure) and crypto-shredding is not acceptable.

## Where it fails / limitations
- **Event versioning.** Once consumers exist, you cannot rename or remove a field. Need upcasters / event versioning from day one. Most teams discover this on event #2.
- **GDPR / right-to-erasure.** Append-only stores fight personal-data deletion. Either crypto-shred (encrypt PII per-subject, drop the key) or move PII out of events and reference by ID — neither obvious from the README.
- **Snapshotting bugs.** Stale snapshots + new events with changed semantics = wrong reconstruction. Always rebuild snapshots when event schema changes; the README mentions snapshots as performance, not correctness, hazard.
- **Idempotency on append.** At-least-once delivery causes duplicate appends; need dedup on `(stream_id, expected_version)` optimistic concurrency.
- **Projection drift.** Same as CQRS: read store gets out of sync with events; without a deterministic "rebuild from offset 0" command you ship corrupt reads.
- **Long event streams.** Streams with 100k+ events per aggregate (long-running orders, multi-year accounts) blow memory on naive `replay()` reconstruction.
- **Cross-aggregate consistency.** "Order placed AND payment captured" — never atomic across aggregates. Sagas / process managers required; teams hide this in command handlers and produce ghost states.
- **Debugging.** "Why is this aggregate in state X" requires inspecting an entire event log. Without good tooling (event store CLI, replay debug), troubleshooting is slow.

## Agentic workflow
Drive event-sourcing scaffolding as a five-stage pipeline: (1) an aggregate-design agent identifies bounded context + events from the spec; (2) a code-gen agent emits Event classes (immutable, with `event_id`, `occurred_at`, `aggregate_id`, version), aggregate root with `apply()` + `replay(events)`, repository with `load(id)` + `save(events, expected_version)`; (3) a projection agent emits a projector per query with `position` tracking and idempotent UPSERT; (4) a test agent emits given/when/then tests where `given = list[Event]`, `when = command`, `then = list[Event]`; (5) a review agent runs anti-pattern checks (mutable events, `setattr` on aggregates outside `apply`, missing `expected_version` on save). Persist event catalog in `.aidocs/product_docs/event-catalog.md`. Use `faion-sdd-executor-agent` to bind one event/projection/replay-test triple per SDD task.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — opus model fits because event-design choices (granularity, payload, versioning) are decision-heavy and irreversible.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — run before committing event fixtures; events love to carry PII (`shipping_address`, `card_token`) into test snapshots and JSON dumps. Also useful before publishing event schemas to schema registry.
- A purpose-built **event-versioning-gate agent** (worth adding under `agents/`): blocks PRs that modify a published event class without an upcaster and bump in `event_version`. Reads a `.event-catalog.json` to know which classes are published.
- `faion-feature-executor` skill — sequential mode is correct for ES feature slices: event → aggregate `apply` → command handler → projection → test, in that order.
- For CQRS pairing, use sibling `pro/dev/software-developer/cqrs-pattern/` and share the inventory file.

### Prompt pattern
Aggregate design:
```
You are an event-sourcing architect. Given the bounded context spec
in <spec>, output:
1. The aggregate root name and invariants.
2. A list of events as `<EventName>(field: type, ...)`. Events MUST
   include event_id (UUID), occurred_at (UTC datetime), aggregate_id,
   and aggregate_version. Events MUST be past tense and minimal — no
   CRUD-style snapshots.
3. A list of commands; each command produces 1+ events on success or
   raises a domain exception.
4. The reconstruct rule: for each event, the aggregate field updates
   in `apply(<EventName>)`.
Output as the markdown tables in event-sourcing/templates.md. Reject
events that look like state snapshots ("OrderUpdated with full Order").
```

Anti-pattern review:
```
You are reviewing a PR adding event-sourcing code. Flag any of:
(1) Event class with non-frozen dataclass / mutable field,
(2) aggregate method that mutates state outside its `apply` handler,
(3) repository.save without expected_version (optimistic concurrency),
(4) projection without `last_processed_position` tracking or
   non-idempotent write,
(5) command handler that loads aggregate without replaying events
   from store,
(6) edit to a published event class (in event catalog) without an
   upcaster + version bump,
(7) PII in event payload without crypto-shredding plan.
Cite file:line. Do not propose fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `eventstore` CLI / `es` | Append, read, manage projections on EventStoreDB | https://www.eventstore.com/eventstoredb |
| `eventsourcing` (Python) | Aggregate / repository / event-store framework | `pip install eventsourcing` ; https://eventsourcing.readthedocs.io |
| `axon-cli` | Inspect / replay events on Axon Server | https://docs.axoniq.io |
| `kafka-console-consumer` / `kcat` | Inspect Kafka-backed event streams, replay from offset | https://github.com/edenhill/kcat |
| `nats` CLI + JetStream | Lightweight event store for small footprints | https://nats.io |
| `Marten` CLI tasks | Postgres-backed CQRS+ES; `dotnet marten projection rebuild` | https://martendb.io |
| `Debezium` | CDC from RDBMS to event log when refit isn't an option | https://debezium.io |
| `dbt` | Build read-model projections as SQL models from append-only event tables | https://docs.getdbt.com |
| `faktory` / `Temporal` CLI | Saga / process manager orchestration around event store | https://temporal.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| EventStoreDB | OSS + cloud | yes | Purpose-built event store; HTTP+gRPC APIs; built-in projections. |
| Axon Server | Commercial + free dev tier | yes | Bus + event store for JVM stacks. |
| Marten (Postgres) | OSS | yes | ES on Postgres — single-DB simplicity, ideal for small-team. |
| Apache Kafka + Schema Registry | OSS / Confluent SaaS | yes | Event log + projection sinks; high-throughput. |
| NATS JetStream | OSS / Synadia SaaS | yes | Subjects = aggregate streams; cheap to self-host. |
| AWS DynamoDB Streams + Kinesis | SaaS | yes | DDB as event store with Streams as bus; popular serverless ES pattern. |
| MessageDB / Eventide (Postgres) | OSS | yes | Postgres-backed event store with PG NOTIFY-based subscriptions. |
| Apache Pulsar | OSS / StreamNative | yes | Multi-tenant event log; tiered storage solves long retention. |
| Temporal | OSS / Cloud | yes | Owns saga / process-manager layer that ES handlers must NOT own. |
| Apicurio / Confluent Schema Registry | SaaS / OSS | yes | Event schema versioning + compatibility checks; non-optional once >1 consumer. |

## Templates & scripts

The methodology already ships event/aggregate/repository examples in `README.md` and templates in `templates.md`. Gap: an event-catalog lint that blocks breaking changes to published events. Inline drop-in (≤50 lines) — `scripts/event-catalog-lint.py`:

```python
#!/usr/bin/env python3
"""event-catalog-lint.py — block breaking changes to published events.
Usage: event-catalog-lint.py <event-catalog.json> <events-package-path>
event-catalog.json shape:
  {"OrderPlaced": {"version": 1, "fields": ["order_id","customer_id","total"]}}
"""
import ast, json, sys, pathlib
catalog = json.loads(pathlib.Path(sys.argv[1]).read_text())
pkg = pathlib.Path(sys.argv[2])
errs = []
for src in pkg.rglob("*.py"):
    tree = ast.parse(src.read_text())
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef): continue
        if node.name not in catalog: continue
        recorded = catalog[node.name]
        # collect declared fields (dataclass attrs)
        fields = [a.target.id for a in node.body
                  if isinstance(a, ast.AnnAssign) and isinstance(a.target, ast.Name)]
        missing = set(recorded["fields"]) - set(fields)
        renamed = set(fields) - set(recorded["fields"]) - {"event_version"}
        if missing:
            errs.append(f"{src}:{node.lineno} {node.name} dropped fields {sorted(missing)} "
                        f"— add upcaster, bump event_version")
        if renamed:
            errs.append(f"{src}:{node.lineno} {node.name} new fields {sorted(renamed)} "
                        f"— bump event_version, add upcaster from v{recorded['version']}")
if errs:
    print("\n".join(errs)); sys.exit(1)
print(f"event-catalog OK ({len(catalog)} events)")
```

Wire into `pre-commit`. The catalog file is committed; renames/drops fail CI until the human acknowledges by bumping `version` and adding an upcaster.

## Best practices
- **Events are past tense, intent-rich, minimal.** `OrderPlaced(order_id, customer_id, items, placed_at)` not `OrderUpdated(...full snapshot...)`. Reject "Updated/Changed" event names.
- **Frozen dataclasses (Python) / records (Java) / immutable C#.** Compile-time guarantee that an event is never mutated after creation.
- **Stable event IDs from the producer.** UUIDv7 (time-ordered) so projections can dedup and order across consumers.
- **Optimistic concurrency on append.** `repository.save(stream_id, events, expected_version)` — fail fast on conflict, retry the command from the new state. Without this you get ghost writes.
- **Projections track position + are idempotent.** `(stream_id, position)` PK on the projection's checkpoint table; UPSERT on apply.
- **Snapshot every N events (50–100), but treat as cache.** Always able to reconstruct from event 0; snapshots are a perf optimization, never source of truth.
- **PII out of events or crypto-shred.** Either reference `customer_id` (and store PII in a mutable side table that respects GDPR) or encrypt PII fields per-subject and discard the key on erasure request.
- **Event catalog is committed source.** A `.event-catalog.json` (or schema registry export) lives in the repo; CI fails on incompatible changes.
- **One event per command success.** Multi-event commands are a smell — usually the command should be split into two commands.
- **Replay tests as default.** `given_events → when_command → then_events` is the canonical test shape; agents naturally produce them when the prompt enforces it.
- **Schedule projection rebuilds.** Nightly job rebuilds projections from offset 0 in a shadow DB and diffs against live; alerts on drift before users notice.

## AI-agent gotchas
- **CRUD-shaped events.** Agents emit `UserUpdated`, `OrderUpdated`, `OrderUpdated_v2` — flat snapshots. Force naming "what business action happened" + reject `Updated`/`Changed` patterns in lint.
- **Mutating state outside `apply`.** Agents call `self.status = "placed"` in command handlers because it feels natural. The aggregate must mutate state ONLY in `apply(<Event>)` — handlers emit events, replay invokes apply.
- **Forgotten `expected_version`.** Code-gen agents save events without optimistic-concurrency check; replays clobber. Always include `expected_version` parameter in repository signatures.
- **Hallucinated event-store APIs.** Agents invent `event_store.append_one(...)`, `repo.put_events(...)`, `bus.fire(...)`. Pin the exact API in the prompt and provide the imports.
- **Snapshot misuse.** Agents persist current state as a snapshot AND treat it as truth — re-applying events is "skipped if snapshot exists". This breaks event-versioning. Always rebuild snapshot when event schema bumps.
- **Projection writes business logic.** Agents write `if order.total > 1000: send_email(...)` in projection. Projections are passive UPSERTs; emit a domain event for "high-value order" and drive the action from a separate handler.
- **PII leaks into events.** Agents copy command payload directly into events. Force a redact step + a per-event PII-classification field; lint blocks PII without a shred plan.
- **Cross-aggregate handlers.** Agents write `place_order(...)` that loads `Customer`, `Inventory`, `Payment`, mutates all four. That's a saga, not a command handler. Refactor into a process manager.
- **Loose event versioning.** Agents add a field to a published event "to make this query easier". Block: lint must enforce that any field change bumps `event_version` and registers an upcaster.
- **Tests on aggregate getters.** Agents test `aggregate.status == "placed"` after replay. Better: test that `apply(events)` produces the same state as the original aggregate (round-trip) and that command produces expected events list.
- **Human-in-the-loop on event-class deletion.** Deleting / renaming an event must be human-reviewed because external consumers depend on the schema. Never auto-merge.

## References
- Fowler, M. "Event Sourcing." https://martinfowler.com/eaaDev/EventSourcing.html
- Young, G. "CQRS Documents." https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf
- Vernon, V. "Implementing Domain-Driven Design," ch. 8 (Domain Events).
- Helland, P. "Immutability Changes Everything." https://queue.acm.org/detail.cfm?id=2884038
- Kleppmann, M. "Designing Data-Intensive Applications," ch. 11 (event logs).
- EventStoreDB — Modeling Streams and Subscriptions. https://developers.eventstore.com/server/latest/streams.html
- Marten — Event Sourcing on Postgres. https://martendb.io/events
- Axon Reference Guide — Event Sourcing. https://docs.axoniq.io/reference-guide
- Axon — Event Versioning. https://docs.axoniq.io/reference-guide/axon-framework/events/event-versioning
- Eventide / MessageDB — https://eventide-project.org/
- Sibling methodologies in this repo: `pro/dev/software-developer/cqrs-pattern/`, `pro/dev/code-quality/event-sourcing-basics/`, `pro/dev/code-quality/event-sourcing-implementation/`, `pro/dev/code-quality/cqrs-pattern/`, `pro/dev/code-quality/domain-driven-design/`.
