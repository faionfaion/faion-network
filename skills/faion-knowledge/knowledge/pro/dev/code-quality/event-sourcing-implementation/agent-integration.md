# Agent Integration — Event Sourcing (Implementation)

## When to use
- The team has agreed on event sourcing (see `event-sourcing-basics`) and now needs to ship the *infrastructure*: event store, snapshots, projections, command handlers, replay tooling.
- Migrating from a state-store backend to an event-sourced bounded context (greenfield service or new aggregate type).
- Adding snapshots to an existing event-sourced aggregate where p99 hydration is starting to hurt.
- Building a new projection (read model) on top of an existing event log.
- Hardening an existing implementation: optimistic concurrency, idempotent consumers, replay tooling, schema versioning.

## When NOT to use
- You haven't designed the events yet — go back to `event-sourcing-basics` first.
- You're prototyping; the implementation in this README assumes a real Postgres + production tooling. For a spike, use Marten or in-memory.
- Single-process, single-writer system that fits in a SQLite + audit table — implementation tax is not justified.
- Hot-path with sub-1ms latency and >100k writes/s — append + version-check + serialization adds latency; consider Kafka log-as-store with custom ordering instead.
- The team can't operate Postgres (or chosen backend) — event store ops cost is real (vacuum, partitioning, archival).

## Where it fails / limitations
- **Concurrency-check race.** The naive `SELECT MAX(version) … then INSERT` shown in the README has a race between two writers; in production use a single `INSERT … ON CONFLICT (stream_id, version) DO NOTHING` with a unique constraint, or wrap in serializable txn — otherwise duplicate-version inserts succeed under load.
- **Projection lag visibility.** `EventBus.publish` after `_repository.save` ties projections to the command path — a slow projection blocks writes. In production, decouple via outbox + async projector; lag becomes the new SLI.
- **Snapshot frequency = 50 is a guess.** The right cadence depends on event size and replay budget. Measure first; some aggregates need 5, some 5000.
- **Serializer drift.** The `_serializers` registry pattern silently breaks when class names change (refactor → renamed → deserialize fails). Use explicit `event_type` strings, not `type(event).__name__`.
- **No upcasting.** The `_deserialize` path assumes today's schema fits yesterday's events. Real systems need an upcaster pipeline keyed on `(event_type, version)`.
- **Replay scalability.** `read_all` paginated by 100 won't scale past ~10M events; you need partitioned replay (by stream prefix or time bucket).
- **Snapshot consistency.** If a snapshot is written but the events fail (or vice versa), you have torn state. Persist snapshot + events in a single transaction or accept "snapshot is best-effort, ground truth is the event log."
- **Outbox pattern missing.** README publishes events to projections from the command path, not from the event store via outbox. That couples write availability to read-model availability.

## Agentic workflow
Drive event-sourcing implementation as a four-pass pipeline: (1) a scaffolding agent generates the event store schema, repository, and snapshot store from the chosen backend (Postgres / EventStoreDB / Marten); (2) a projection-generator agent reads `domain/events/` and creates a projection class + DDL per read model; (3) a property-test agent generates `hypothesis`-style invariants ("any sequence of valid commands → aggregate state matches projection state"); (4) a replay-harness agent builds a CLI to rebuild a given projection from scratch, with checkpoints. All passes must be reviewed by a human before merge — concurrency code is where agents most often produce subtly broken systems.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — implement event-store / projection / replay tasks as SDD items with quality gates: every PR must add a property test and a replay command.
- A purpose-built **concurrency-test agent** (worth creating): generates `pytest-asyncio` tests that fork N writers against the same stream and assert exactly one wins per version slot.
- A purpose-built **projection-rebuild agent** (worth creating): given a projection class, emit `python -m projections.rebuild --projection orderdetails --from 0 --batch 1000` with checkpointing.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — events stored in Postgres often contain PII; scrub dumps before sharing.

### Prompt pattern
Concurrency hardening:
```
Audit this PostgresEventStore.append for race conditions. Refactor
to use a unique (stream_id, version) constraint and ON CONFLICT
DO NOTHING; on conflict, raise ConcurrencyError. Add a pytest
that runs 50 concurrent appends against the same stream and
asserts exactly one succeeds per version slot.
```

Projection scaffolding:
```
For event class <X> in domain/events/, generate a no-op handler in
every existing projection under projections/. Then in projections/
<projection>.py emit the SQL UPSERT consistent with the projection
schema. Reject the change if the projection has no idempotency key.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `psql` | Inspect / query event store and projection tables | bundled |
| `pgcli` | REPL for Postgres event store with autocomplete | `pip install pgcli` |
| Alembic / Flyway | Migrate event-store schema (events, snapshots, projections) | https://alembic.sqlalchemy.org / https://flywaydb.org |
| `pg_dump --table=events` | Backup event log (forever-data; back up daily) | bundled |
| `wal-g` / `pgbackrest` | Continuous archive — events are the source of truth | https://github.com/wal-g/wal-g |
| `pgbouncer` | Connection pooling for high-write event-store workloads | https://www.pgbouncer.org |
| `pg_partman` | Time-partitioning for `events` table at scale | https://github.com/pgpartman/pg_partman |
| `kafka-console-consumer` / `rpk topic consume` | Inspect outbox topic when using outbox-to-Kafka | bundled with Kafka / Redpanda |
| Debezium CDC | Stream Postgres `events` table → Kafka outbox | https://debezium.io |
| `claude` (Anthropic CLI) | Run scaffolding / property-test / replay-harness passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostgreSQL (self-host or RDS) | OSS / SaaS | yes | Default backend for the README's pattern. Cheapest path to production. |
| EventStoreDB | OSS + SaaS (Kurrent Cloud) | gRPC API yes | Purpose-built; subscriptions and replay built-in. |
| Marten on PostgreSQL | OSS | yes (.NET) | Drop-in event store + document DB. Lowest ops tax for solo. |
| Axon Server | OSS + commercial | REST/gRPC | Event store + command bus + saga; tied to Axon Framework (JVM). |
| Apache Kafka + Schema Registry | OSS / Confluent | yes | Log-as-event-store; you build snapshots and aggregate replay yourself. |
| AWS DynamoDB + Streams | SaaS | API yes | Cheap at scale; DIY snapshot + projection. |
| Confluent Cloud | SaaS | yes | Managed Kafka with Schema Registry; good for high-throughput EDA. |
| Debezium | OSS | yes | Outbox pattern via CDC from Postgres → Kafka. Production must-have if you publish externally. |
| Temporal.io | OSS + SaaS | SDK | Workflow engine; covers process-manager / saga concerns over your event store. |
| Snowflake / BigQuery | SaaS | yes | Long-term analytical projection of event log via CDC. |

## Templates & scripts
The README ships event store / snapshot / projection / command handler code. The high-leverage missing piece is a deterministic **replay harness** to rebuild projections. Inline drop-in (≤50 lines):

```python
#!/usr/bin/env python3
# replay.py — rebuild a projection from event log with checkpoints.
# Usage: python replay.py --projection order_details --batch 1000
import asyncio, argparse, importlib, sys
from infrastructure.event_store import get_event_store
from infrastructure.db import get_session

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--projection", required=True)
    ap.add_argument("--from", dest="from_pos", type=int, default=0)
    ap.add_argument("--batch", type=int, default=1000)
    args = ap.parse_args()

    mod = importlib.import_module(f"projections.{args.projection}")
    proj = mod.build(get_session())
    store = get_event_store()
    pos = args.from_pos
    print(f"replaying {args.projection} from {pos}")
    await proj.truncate()  # or use shadow table + atomic swap
    while True:
        batch = await store.read_all(from_position=pos, batch_size=args.batch)
        if not batch:
            break
        for event in batch:
            handler = getattr(proj, f"handle_{type(event).__name__.lower()}", None)
            if handler:
                await handler(event)
        pos += len(batch)
        if pos % (args.batch * 10) == 0:
            print(f"  pos={pos}")
    print(f"done, final pos={pos}")

if __name__ == "__main__":
    asyncio.run(main())
```

Pair with a **shadow-table swap** so production keeps reading the old projection until rebuild finishes.

## Best practices
- **Use a unique constraint, not a SELECT-then-INSERT.** Optimistic concurrency belongs in the database (`UNIQUE(stream_id, version)`) — anything else races.
- **Outbox or bust.** Don't publish projections from the command handler; write events + outbox row in one transaction; a separate worker drains the outbox. This decouples write availability from projection availability.
- **Idempotent projections.** Every projection upsert must use `ON CONFLICT … DO UPDATE` keyed on event id, so re-replays don't double-count.
- **Versioned event types.** Store `event_type=OrderPlaced.v2`; deserialization keys on (type, version). Add an upcaster registry from day one — retrofitting it later is brutal.
- **Partition events at scale.** Use `pg_partman` by `occurred_at` once `events` exceeds ~50M rows; otherwise vacuum and bloat eat you alive.
- **Snapshot in a separate transaction.** Snapshot is a cache; if it fails, hydration falls back to full replay. Never block command commit on snapshot writes.
- **Replay must be a CLI.** "Just rerun the projector" only works if there's an idempotent CLI with `--from`, `--projection`, `--shadow` flags and structured logs.
- **Backup is non-negotiable.** Events are forever; lose them and you lose the company. Continuous archive (wal-g) + monthly restore tests.
- **Schema registry for cross-service events.** If events leave the bounded context, register them — at minimum a JSON Schema in a `events-contracts/` repo, ideally Confluent Schema Registry or Buf BSR.

## AI-agent gotchas
- **Race-condition blind spots.** Agents replicate the README's `SELECT MAX(version) … INSERT` pattern verbatim, which races. Always require a unique constraint + `ON CONFLICT` and a concurrency test.
- **Type-name as key.** `type(event).__name__` is the default; agents won't add an explicit `event_type` registry. Renaming a class then breaks deserialization silently. Force a `class Event: __event_type__ = "OrderPlaced.v1"` convention.
- **Forgotten serializer.** Agents register a few serializers and use `__dict__` fallback for the rest; non-trivial fields (`Decimal`, `datetime`, value objects) round-trip wrong. Require explicit serializer per event class.
- **Async-sync mix.** Agents call sync ORM methods inside `async def` handlers, deadlocking under load. Lint for `Session` (sync) vs `AsyncSession`.
- **`await self._session.commit()` per event.** Generated code commits inside the loop, not after the batch; throughput tanks. Commit once after the whole append.
- **Projection coupled to command.** Agents publish to `EventBus` from the command handler, not from the outbox. Fail review when no `outbox` table exists.
- **Replay without truncate.** Generated rebuild scripts run handlers on top of dirty data and double-count. Require explicit `truncate()` or shadow-table swap.
- **Snapshot without version.** Agents store `state` JSON without a `schema_version`. When the aggregate shape changes, snapshots crash on load. Hard-require `schema_version` field.
- **No human checkpoint on backfill.** A bad replay can wipe a production read model. Backfills run in a shadow table; promotion is a human-gated atomic rename.
- **Hallucinated SQL dialects.** Agents mix `JSONB` (Postgres), `JSON` (MySQL), and `JSON_VALUE` (SQL Server) in the same migration. Pin the backend in repo docs and grep generated SQL.

## References
- Young, G. — "Versioning in an Event Sourced System" (free book). https://leanpub.com/esversioning
- EventStoreDB docs — projections, subscriptions, replay. https://developers.eventstore.com
- Marten Events docs. https://martendb.io/events/
- Microsoft — "Outbox pattern." https://learn.microsoft.com/azure/architecture/patterns/transactional-outbox
- Debezium — "Reliable Microservices Data Exchange With the Outbox Pattern." https://debezium.io/blog/2019/02/19/reliable-microservices-data-exchange-with-the-outbox-pattern/
- Kleppmann, M. — "Designing Data-Intensive Applications," Ch. 11. O'Reilly, 2017.
- pg_partman — Postgres partitioning. https://github.com/pgpartman/pg_partman
- Sibling: `pro/dev/code-quality/event-sourcing-basics/` (this batch) — design.
- Sibling: `pro/dev/code-quality/cqrs-pattern/` — read/write separation.
- Sibling: `pro/dev/software-architect/event-driven-architecture/` (this batch) — broader EDA context.
