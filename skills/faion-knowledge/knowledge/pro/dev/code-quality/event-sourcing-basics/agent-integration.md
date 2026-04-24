# Agent Integration — Event Sourcing (Basics)

## When to use
- Domain has a clear, business-meaningful event vocabulary (Order, Payment, Account) — not a generic CRUD app.
- Audit trail is a hard requirement: regulator, finance, healthcare, legal, supply-chain.
- "Show state as of date X" is a real query (subscriptions, accounting periods, billing reversals).
- You need event replay to seed downstream systems (search index, ML feature store, CDC consumers).
- You already use DDD aggregates and your team is comfortable with the vocabulary.
- Greenfield bounded context where you control persistence end-to-end.

## When NOT to use
- CRUD app with no temporal, audit, or replay needs — use plain rows + an audit table.
- Team has never shipped event-driven code; the conceptual tax is high (mutable→immutable, current state→fold).
- Schema is volatile and nobody owns event versioning — events are forever; bad schemas haunt you.
- Hard requirement for synchronous cross-aggregate ACID writes — eventual consistency between projections is the norm.
- Reporting needs are simple SQL — projections add latency and operational overhead vs. a normalized table.
- Tooling is unbudgeted (event store, snapshot store, projector, idempotent consumers, replayer, schema registry).

## Where it fails / limitations
- **Event schema drift.** Once written, events live forever. v2 of `OrderPlaced` must coexist with v1; without an upcaster registry the aggregate's `_apply` becomes a switch-statement of regret.
- **Replay storms.** Rebuilding a projection from 100M events on a single consumer can take days; you need parallel partitioned replay or it never finishes.
- **Snapshot rot.** Snapshots serialize the current shape of state; when state shape changes (renamed field, new value object) old snapshots crash on load. Either version snapshots or invalidate them.
- **Hidden coupling via shared events.** Events become a public API across services. A "small" rename breaks every downstream consumer silently.
- **Aggregate bloat.** A long-lived aggregate (a customer with 10 years of events) gets slow even with snapshots; sometimes you need to close-and-reopen streams.
- **Cross-aggregate invariants.** Event sourcing protects invariants inside one aggregate. Spanning constraints (uniqueness across aggregates) require a process manager or unique-index projection — not free.
- **Test cost.** "Given these events, when this command, then those events" is great in theory. In practice agents generate test fixtures with subtly wrong event order or missing causation IDs.

## Agentic workflow
Drive event sourcing as a multi-pass design pipeline: (1) a domain-modeling agent runs an Event Storming session over a feature spec and produces a candidate event list with aggregate boundaries; (2) a code-generation agent emits frozen `@dataclass` events, an aggregate skeleton, and `_on_*` handlers from that list; (3) a test-generation agent writes given/when/then aggregate tests covering each command path; (4) a reviewer agent verifies events are immutable (`frozen=True`), past-tense, named after business outcomes (not CRUD verbs), and that each command produces ≥1 event. Persist the event catalog as `domain/events/CATALOG.md` and re-run pass (4) on every PR that touches `domain/events/**`.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — execute event-modeling tasks as SDD items, with quality gates ensuring each command-handler test asserts the expected event sequence.
- A purpose-built **event-storming agent** (not yet in repo): given a feature spec, emit `events.md` with columns `Event | Trigger | Aggregate | Invariants | Downstream consumers`.
- A purpose-built **schema-evolution reviewer** (worth creating): on PRs that modify `domain/events/`, fail if a field is removed/renamed without a `Vn` companion class and an upcaster.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — events sometimes carry PII (email, address payloads) — scrub before sharing fixtures externally.

### Prompt pattern
Event discovery:
```
Given this feature spec <spec>, run Event Storming. Output:
1) timeline of past-tense events (e.g. OrderPlaced, not PlaceOrder)
2) for each event: producer aggregate, payload fields, downstream
   read models. Reject events that look like CRUD ("UserUpdated"
   is banned — name the actual change: EmailChanged).
```

Aggregate scaffolding:
```
Generate an event-sourced Order aggregate in Python following the
README pattern: frozen dataclass events, _apply dispatcher, _on_*
handlers, factory `create`, `from_events`, `collect_pending_events`.
For each business rule in <spec>, add a command method that raises
DomainError on invalid state and emits exactly one event.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| EventStoreDB CLI (`es`) | Append, read, subscribe streams from terminal | https://developers.eventstore.com |
| `psql` + `events` table | Quick-look at events / streams in PostgreSQL backed stores | bundled |
| `protoc` + `buf` | Schema-validate event payloads (protobuf) and detect breaking changes in CI | https://buf.build |
| `jq` | Inspect JSON event payloads in dump files | `apt install jq` |
| `kafkactl` / `rpk` | When events live on Kafka / Redpanda | https://github.com/deviceinsight/kafkactl ; https://docs.redpanda.com/current/get-started/rpk-install/ |
| `axon-cli` | Query/replay Axon Framework event streams (JVM) | https://docs.axoniq.io |
| `eventstore-tcp`/`grpc` clients | Programmatic replay/projection rebuild | language-specific SDKs |
| `claude` (Anthropic CLI) | Headless event-storming & test-generation passes | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| EventStoreDB | OSS + commercial cloud | gRPC API yes | Purpose-built event store with subscriptions, projections (JS), replay. |
| Marten (Postgres) | OSS | yes (.NET) | Event store + document DB on PostgreSQL; great for solo / mid-scale. |
| Axon Server | OSS + commercial | REST/gRPC | Event store + command bus + saga; tied to Axon Framework. |
| Kurrent (was EventStore Cloud) | SaaS | API yes | Managed EventStoreDB; pay-per-stream. |
| AWS DynamoDB + Streams | SaaS | API yes | DIY event store pattern; cheap at scale, pay only for what you use. |
| Apache Kafka + ksqlDB | OSS / SaaS | API yes | Log-as-event-store; works but you build snapshots and aggregate replay yourself. |
| MartenDB Cloud / self-host | OSS | yes | Postgres-backed; lowest operational tax for solo founders. |
| EventStoreDB on fly.io / Hetzner | self-host | yes | Cheap dedicated host; 5GB+ event volumes fit easily. |
| `prooph` / Broadway / Equinox | OSS frameworks | yes | Per-language event sourcing libs (PHP / .NET / F#). |

## Templates & scripts
The methodology already ships event/aggregate/test code in `examples.md` and `templates.md`. The gap is a lint pass that catches the common modeling mistakes. Inline drop-in (≤50 lines):

```python
#!/usr/bin/env python3
# event_lint.py — fail CI on event-sourcing anti-patterns.
# Usage: event_lint.py domain/events/
import ast, pathlib, sys, re

BANNED = {"Updated", "Changed", "Modified", "Set"}  # too generic
MUST_FROZEN = re.compile(r"@dataclass\(frozen=True\)")
errs = []

for f in pathlib.Path(sys.argv[1]).rglob("*.py"):
    src = f.read_text()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and any(
            isinstance(b, ast.Name) and b.id == "Event" for b in node.bases
        ):
            # past-tense check (heuristic): ends with "ed" or "ted"
            if not (node.name.endswith("ed") or node.name.endswith("d")):
                errs.append(f"{f}:{node.lineno} {node.name}: not past tense")
            # banned generic suffixes
            for b in BANNED:
                if node.name.endswith(b) and len(node.name) <= len(b) + 4:
                    errs.append(f"{f}:{node.lineno} {node.name}: too generic ({b})")
            # frozen=True check
            decos = [ast.unparse(d) for d in node.decorator_list]
            if not any("frozen=True" in d for d in decos):
                errs.append(f"{f}:{node.lineno} {node.name}: not frozen")
for e in errs:
    print(e)
sys.exit(1 if errs else 0)
```

Wire into pre-commit on any repo with `domain/events/`.

## Best practices
- **Past-tense, business-meaningful names.** `OrderPlaced`, not `OrderUpdated`. Banned suffixes: `Updated`, `Changed`, `Set` — they hide *what* changed.
- **One event per business fact.** Don't pack "place + ship" into one event; downstream consumers can't subscribe to half of it.
- **Causation + correlation IDs in metadata.** Every event carries `correlation_id` (the request) and `causation_id` (the prior event). Without them, multi-aggregate flows are undebuggable.
- **Events are forever.** Treat the event schema as a public API: never delete fields, only deprecate. Add `_v2` classes, never mutate `_v1`.
- **`_apply` must be pure.** No I/O, no `datetime.utcnow()` (use `event.occurred_at`), no calls to other aggregates. Replay must be deterministic.
- **Snapshot policy = a tunable, not a feature.** Start without snapshots; add them when load tests show p99 hydration > target.
- **Stream-per-aggregate.** Don't share streams across aggregate types; you'll regret it at replay time.
- **Project, don't query.** Never run `SELECT … FROM events WHERE …` for reads; build a projection. Querying the event store directly is the highest-cost operation.

## AI-agent gotchas
- **CRUD-leak in event names.** LLMs default to `UserUpdated` / `OrderModified` because that's what's in training data. Force past-tense + business outcome via the prompt and a lint rule.
- **Mutable events.** Agents will write `@dataclass` (without `frozen=True`) and then mutate fields in handlers. Lint for `frozen=True` and reject PRs without it.
- **Apply-handlers with side effects.** Agents add `await event_bus.publish(...)` inside `_on_*`. That breaks replay. Apply must be pure; publishing happens in the command handler after `repository.save`.
- **Forgotten projections.** Agents emit new events but never update read-model projections. Add a generation pass that, for each new event class, scaffolds a no-op handler in every existing projection and fails CI if missing.
- **Snapshot version mismatch.** When the agent renames an aggregate field, snapshots break silently. Hard rule: bump `Order.SCHEMA_VERSION` and invalidate older snapshots, or write an upcaster.
- **Test fixtures missing causation chain.** Generated `from_events` test setups omit `correlation_id` / `causation_id`, hiding bugs in saga handlers. Require both fields in fixture builders.
- **Hallucinated event store APIs.** Agents mix EventStoreDB v5 / v20 / Marten / Axon APIs in the same file. Pin the chosen library in `pyproject.toml` and grep generated imports.
- **Large events.** Agents pack the entire aggregate state into a single `OrderUpdated` event "for completeness". Reject; require event classes < ~10 fields.
- **No human checkpoint on schema deletion.** Removing or renaming a field on a stored event is a destructive change disguised as a refactor — never let an autonomous agent merge it.

## References
- Fowler, M. — "Event Sourcing." https://martinfowler.com/eaaDev/EventSourcing.html
- Young, G. — "CQRS Documents." https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf
- Vernon, V. — "Implementing Domain-Driven Design." Addison-Wesley, 2013.
- EventStoreDB docs. https://developers.eventstore.com
- Marten Events docs. https://martendb.io/events/
- Brandolini, A. — "Introducing EventStorming." https://www.eventstorming.com
- Sibling methodology: `pro/dev/code-quality/event-sourcing-implementation/` (this batch).
- Sibling methodology: `pro/dev/code-quality/cqrs-pattern/`.
