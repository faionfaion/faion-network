# Agent Integration — Data Modeling

## When to use
- Greenfield schema design: agent goes from business entities → conceptual → logical → physical model with constraints, indexes, and migrations.
- Adding a new bounded context to an existing schema; agent designs new tables/collections and the contract with existing models.
- Translating between paradigms: relational → document, document → wide-column, OLTP → OLAP star/snowflake/Data Vault 2.0.
- Slowly Changing Dimensions (SCD) Type-2 / Type-6 implementations for analytics warehouses.
- Polyglot persistence layout: where each entity lives (PG vs Redis vs Elasticsearch vs vector DB) and how they synchronize.

## When NOT to use
- Trivial CRUD app with 3-5 tables that any junior dev would model the same way — overhead exceeds value.
- Pure migration scripting where the schema is already decided — that's `database-selection` follow-up + ORM tooling.
- Performance tuning of an existing model (indexes, partitions) — that's a separate optimization task.
- Vector embedding storage decisions — those go to `database-selection` and embedding-design discussions.

## Where it fails / limitations
- LLMs default to relational/3NF and over-normalize, then ignore the join cost on hot paths.
- For document stores, agents either embed everything (16 MB cliff) or reference everything (N+1 query graveyard); rarely the right hybrid.
- Wide-column (Cassandra/Scylla) needs query-first design — agent draws ER diagrams instead and produces unworkable schemas.
- Time-series modeling: tag vs field choice, retention policy, continuous aggregates — agents skip these and recommend "just use TimescaleDB".
- Graph models: agents conflate nodes/relationships with row/foreign-key thinking and produce poor traversal patterns.
- SCD: agents pick Type-2 by default for everything, doubling row counts unnecessarily.
- Cardinality and optionality (1:1 vs 0..1, M:N junction tables) often hand-waved.

## Agentic workflow
Sonnet for the conceptual + logical phases (requires domain reasoning), haiku for physical schema generation from `templates.md`, opus only for novel paradigms (Data Vault, graph for fraud, time-series with multiple resolution windows). Run a 3-pass: pass 1 = entities + relationships in plain English; pass 2 = logical model with attributes, keys, cardinality; pass 3 = physical DDL/BSON/CQL with indexes, constraints, partitions. Pair with `database-selection` (DB has been chosen) and `caching-architecture` (read paths). End with realistic seed data and 5 query patterns the model must serve in <10ms.

### Recommended subagents
- `faion-sdd-executor-agent` — owns the modeling task in SDD: spec, design, migration files, test data, ADR for non-trivial choices.
- `faion-feature-executor` — runs sequential migration tasks (per-table or per-context) with quality gates.
- `faion-improver` — tracks recurring modeling mistakes (over-normalization, embedded too deep) for future prevention.

### Prompt pattern
```
Design data model for <feature> in <PostgreSQL 16 / MongoDB 7 / Cassandra 5 / TimescaleDB / Neo4j>.
Business entities: <list with one-line description>. Relationships: <list>.
Access patterns (top 10, with frequency and latency target):
  1. <pattern> — <reads/sec> — <p95 latency>
  ...
Scale: <rows / docs / events at 12mo>.
Output: conceptual ER (Mermaid), logical model (entities + attrs + keys + cardinality),
physical DDL with indexes/constraints/partitions, sample seed data (10 rows per table),
EXPLAIN-style query plan for top 5 access patterns. Flag anything you assume.
```

```
Convert this 3NF PostgreSQL schema to a MongoDB document model optimized for these
access patterns: <list>. Show: target collections, embed-vs-reference decisions per
relationship, indexes, schema validator JSON. Flag any pattern that becomes >10x slower.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pgcli` / `psql` | PostgreSQL inspect, EXPLAIN ANALYZE | `pip install pgcli` |
| `mysql` / `mycli` | MySQL inspect | `pip install mycli` |
| `mongosh` | MongoDB shell, schema validator dev | https://www.mongodb.com/try/download/shell |
| `cqlsh` | Cassandra/Scylla CQL shell | bundled in Cassandra |
| `cypher-shell` | Neo4j queries | https://neo4j.com/download-center/ |
| `dbml-cli` | DBML → SQL/MongoDB/etc. | `npm i -g @dbml/cli` |
| `atlas` (ariga) | Schema-as-code, diffs, migrations | https://atlasgo.io/ |
| `Liquibase` / `Flyway` | Versioned migrations | https://www.liquibase.org/ / https://flywaydb.org/ |
| `pgmodeler` | ERD authoring | https://pgmodeler.io/ |
| `mermaid-cli` | Render ER diagrams to SVG/PNG | `npm i -g @mermaid-js/mermaid-cli` |
| `dbdiagram.io` (web) | Quick DBML ERD | https://dbdiagram.io |
| `pg_partman` / `timescaledb` extensions | Partitioning, hypertables | shipped with PG/TS |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| dbt | OSS+SaaS | Yes | Logical models in SQL; agent emits models + tests + docs. |
| Hackolade | Desktop | Partial | Multi-paradigm modeling; primarily UI-driven. |
| Atlas Cloud | SaaS | Yes | Schema CI; PR diffs and auto-migrations. |
| SqlDBM | SaaS | Partial | UI-first; some import/export. |
| Coalesce | SaaS | Partial | Data Vault automation; UI-heavy. |
| dbdocs.io | SaaS | Yes | DBML → hosted docs; agent commits `.dbml` and CI builds. |
| Schema Spy | OSS | Yes | Static HTML doc gen from existing DB. |
| Snowflake / BigQuery / Redshift | SaaS | Yes | OLAP targets; agent emits star schema DDL. |

## Templates & scripts
See `templates.md` for PostgreSQL, MongoDB, Cassandra, Neo4j, TimescaleDB starters. Inline DBML-to-Mermaid converter (single-file, agent loop friendly):

```python
#!/usr/bin/env python3
# dbml_to_mermaid.py — quick ER diagram from DBML for ADRs.
import re, sys
src = open(sys.argv[1]).read()
print("erDiagram")
for m in re.finditer(r'Table\s+(\w+)\s*\{([^}]*)\}', src):
    t, body = m.group(1), m.group(2)
    cols = [l.strip().split() for l in body.strip().splitlines() if l.strip()]
    print(f'  {t} {{')
    for c in cols:
        if len(c) >= 2:
            print(f'    {c[1]} {c[0]}')
    print('  }')
for m in re.finditer(r'Ref:\s+(\w+)\.\w+\s*([<>-])\s*(\w+)\.\w+', src):
    a, op, b = m.group(1), m.group(2), m.group(3)
    rel = '||--o{' if op == '<' else '}o--||'
    print(f'  {a} {rel} {b} : ref')
```

## Best practices
- Start with access patterns, not entities. List the top 10 reads/writes with frequency and latency target before drawing any schema.
- Normalize OLTP to 3NF, denormalize for known hot reads, document why each denormalization exists.
- Make every table have `id`, `created_at`, `updated_at`, soft-delete or audit columns from day one — adding later is painful.
- Constraints in the DB, not the app: `NOT NULL`, `CHECK`, `FOREIGN KEY`, unique indexes; the agent must include these in every DDL.
- Partition early on append-only tables (events, logs, time-series); retrofitting partitioning is a maintenance window.
- For document DBs, embed when "always queried together and updated together"; reference everything else.
- For wide-column, write one table per query pattern — no "general purpose" tables.
- Migrations in version control with up + down (or forward-only with explicit notes); agent emits both.

## AI-agent gotchas
- LLMs add `text` columns where `varchar(n)` or `enum` is correct; demand the smallest valid type.
- Agents skip composite primary keys in junction tables — leading to silent duplicates.
- `created_at TIMESTAMP DEFAULT NOW()` without timezone — almost always wrong; demand `TIMESTAMPTZ`.
- MongoDB schema validators are agent-skippable; require `$jsonSchema` on every collection.
- Cassandra: agent uses generic `id uuid PRIMARY KEY` partition key, leading to hot partitions; force a real partition strategy.
- Neo4j: agent stores everything as node properties; reject when properties should be relationships (e.g., `manager: <node-id>`).
- TimescaleDB: agent forgets `create_hypertable()` and continuous aggregates; require both.
- Indexes: agent adds an index per WHERE clause without considering write amplification; demand a compound-index analysis.
- ORM-driven generation (Django, SQLAlchemy, Prisma) hides constraints; always emit raw DDL alongside ORM models for review.
- Data lineage: agent skips it for analytics models; require source-of-truth annotation per column.

## References
- Kleppmann, M. (2017). "Designing Data-Intensive Applications."
- Date, C. J. "An Introduction to Database Systems."
- Linstedt & Olschimke (2015). "Building a Scalable Data Warehouse with Data Vault 2.0."
- Kimball & Ross. "The Data Warehouse Toolkit" (Type 1-6 SCD).
- Pramod Sadalage & Martin Fowler. "NoSQL Distilled."
- MongoDB Schema Design Patterns — https://www.mongodb.com/blog/post/building-with-patterns-a-summary
- DataStax Cassandra Data Modeling — https://www.datastax.com/learn/data-modeling-by-example
- Neo4j Graph Modeling Guidelines — https://neo4j.com/docs/getting-started/data-modeling/guide-data-modeling/
- TimescaleDB best practices — https://docs.timescale.com/use-timescale/latest/schema-management/
- DBML reference — https://dbml.dbdiagram.io/docs/
