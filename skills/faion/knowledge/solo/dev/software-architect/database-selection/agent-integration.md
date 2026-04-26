# Agent Integration — Database Selection

## When to use
- Greenfield system: agent must pick the primary OLTP store and any companion datastores (cache, search, vector, time-series).
- Adding a new bounded context to an existing system that doesn't fit the current DB (RAG over docs, analytics, event log).
- Migrations: MySQL → PostgreSQL, monolith DB → polyglot persistence, single-region → globally distributed.
- Cost optimization: comparing managed vs self-hosted, RDS vs Aurora vs CockroachDB Serverless vs Neon, with concrete TCO over 1-3 years.
- Vector DB picks for RAG pipelines (Qdrant / Weaviate / pgvector / Pinecone / Milvus) given embedding count, filter complexity, and ops budget.

## When NOT to use
- "What database should I use for my SaaS?" without requirements — agent will pick PostgreSQL by default and be right 80% of the time; deeper analysis only if there's a specific access pattern, scale, or regulatory constraint.
- Pure performance tuning of an already-chosen DB — that's `data-modeling`, `caching-architecture`, or DBA work, not selection.
- Picking a DB to satisfy resume-driven curiosity ("can I use Cassandra?") — agent should challenge the brief.

## Where it fails / limitations
- LLMs cite outdated pricing, region availability, and feature gaps; treat any specific number as suspect.
- Agents over-recommend MongoDB for "flexibility" when the data is clearly relational and joins will be needed within a release.
- CAP/PACELC explanations from LLMs are usually correct in theory but misapplied to specific products (PostgreSQL "CA" — only on a single node).
- Vector DB recommendations rarely account for filter cardinality, hybrid search needs, or update/delete patterns.
- Time-series picks ignore retention policy, downsampling, and continuous aggregates which dominate ops cost.
- Agents skip the "what if we pick wrong?" question; reversibility is the most important hidden criterion.

## Agentic workflow
This is a high-stakes Type-1 decision — drive with opus on the final pick, sonnet for shortlisting, haiku for filling decision matrices from `templates.md`. Run as a 3-step pipeline: 1) requirements extraction (entities, access patterns, scale, consistency, regulatory), 2) shortlist of 2-3 candidates with explicit trade-offs, 3) ADR with the chosen DB plus migration / fallback plan. Always pair with `trade-off-analysis` and `data-modeling` methodologies in context. End every selection with a "validate with a 1-week prototype" task.

### Recommended subagents
- `faion-sdd-executor-agent` — turns the selection into an SDD feature: spec, ADR, migration plan, test plan.
- `faion-brainstorm` — diverge/converge on candidate set; particularly useful for vector DB and time-series picks where 5+ products compete.
- `faion-improver` — pulls past DB decisions from `.aidocs/memory/decisions.md` so agents don't relitigate.

### Prompt pattern
```
Select primary OLTP database for <system>. Requirements:
- Entities + access patterns: <bullets>
- Scale: <reads/sec, writes/sec, GB now / 12mo / 36mo>
- Consistency: <strict / read-after-write / eventual ok>
- Region: <single / multi-region / global>
- Team SQL skill: <none / SQL fluent / DBA on staff>
- Budget: <$/month at year 1>
- Reversibility cost: <effort to switch later>
Output: shortlist of 3, decision matrix with weighted scores, ADR draft for top choice,
list of 5 prototype queries we should run before committing.
```

```
Vector DB pick for RAG with N=<count> embeddings, dim=<d>, filters on <fields>,
update rate=<per day>, ops budget=<low/med/high>. Compare pgvector, Qdrant, Weaviate,
Pinecone. Include cost at 12 months and what breaks at 10x scale.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `psql` / `pgcli` | PostgreSQL inspect, EXPLAIN ANALYZE | `apt install postgresql-client` / `pip install pgcli` |
| `mysql` / `mycli` | MySQL inspect | `apt install mysql-client` / `pip install mycli` |
| `mongosh` | MongoDB shell, agent-driven `db.collection.aggregate` | https://www.mongodb.com/try/download/shell |
| `redis-cli` | Redis ops, key-pattern scans | `apt install redis-tools` |
| `cockroach sql` | CockroachDB shell, supports PostgreSQL wire proto | https://www.cockroachlabs.com/docs/ |
| `tsbs` | Time-series DB benchmark suite (Influx vs Timescale vs ClickHouse) | https://github.com/timescale/tsbs |
| `vector-db-bench` | ANN benchmark across Qdrant/Weaviate/Milvus/pgvector | https://github.com/zilliztech/VectorDBBench |
| `ankane/pghero` | PostgreSQL workload analysis | `gem install pghero` |
| `db-engines` (web) | Cross-DB ranking & feature matrix | https://db-engines.com/ |
| `terraform` + `provider-postgresql` / `mongodbatlas` | Provision & version-control DB infra | https://registry.terraform.io/ |
| `pg_dump` / `mongodump` / `redis-dump-go` | Migration baselines | bundled with each DB |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Amazon RDS / Aurora | SaaS | Yes | CDK/Terraform/CloudFormation; agent must distinguish RDS vs Aurora pricing. |
| Google Cloud SQL / Spanner | SaaS | Yes | gcloud + Terraform; Spanner needs schema design upfront. |
| Neon | SaaS | Yes | Postgres with branching; agent-friendly for ephemeral envs. |
| Supabase | SaaS + OSS | Yes | Postgres + Auth + storage; CLI for migrations. |
| PlanetScale | SaaS | Yes | Vitess MySQL; deploy requests model branching. |
| MongoDB Atlas | SaaS | Yes | Public API, Terraform provider, agent can drive index creation. |
| CockroachDB Cloud | SaaS | Yes | Managed Cockroach; serverless tier for prototyping. |
| Pinecone | SaaS | Yes | Pure REST API; trivial for agent to drive. |
| Qdrant Cloud | SaaS | Yes | OSS underlying; gRPC + REST APIs. |
| Weaviate Cloud | SaaS | Yes | GraphQL + REST; module system for vectorizers. |
| Upstash | SaaS | Yes | Redis/Kafka per-request pricing; agent-friendly for serverless. |
| Turso | SaaS | Yes | libSQL/SQLite at edge; CLI is scriptable. |

## Templates & scripts
See `templates.md` for decision matrix, ADR, migration templates. Inline TCO comparison helper:

```python
#!/usr/bin/env python3
# db_tco.py — rough 12-month TCO for shortlisted databases.
import yaml, sys
cfg = yaml.safe_load(open(sys.argv[1]))  # see templates.md schema
for name, c in cfg["candidates"].items():
    monthly = (
        c["instance_per_month"]
        + c["storage_gb"] * c["price_per_gb"]
        + c["egress_gb_month"] * c["price_per_egress_gb"]
        + c["backup_gb"] * c.get("price_per_backup_gb", 0.05)
    )
    ops_hours = c["ops_hours_per_month"] * c["ops_hourly_rate"]
    print(f"{name:<20} infra=${monthly:8.2f}/mo ops=${ops_hours:8.2f}/mo "
          f"yr1=${(monthly+ops_hours)*12:9.0f}")
```

## Best practices
- Default to PostgreSQL for new systems unless requirements force otherwise; it absorbs document, vector, time-series, and queue workloads via extensions and gives a single ops surface.
- Always quantify: "scale" = reads/sec + writes/sec + GB at 12/24/36 months. Never accept "we need scale" without numbers.
- Reversibility class: if switching the DB later requires >2 weeks of work, treat the decision as Type-1 (deep analysis, ADR, prototype).
- Polyglot persistence is justified only when each store earns its operational cost; agents tend to over-stack — challenge each component.
- For vector DB, filter selectivity matters more than total embedding count; agents must measure filtered-recall not raw ANN recall.
- Run a 1-week prototype with realistic data volume before signing off; agent-generated load scripts (`tsbs`, `vector-db-bench`, custom `k6`) make this trivial.

## AI-agent gotchas
- "I read on a benchmark" — LLMs cite stale benchmarks (Cassandra-vs-Mongo from 2018). Demand a 2024+ source or re-run with `tsbs`/`vector-db-bench`.
- DynamoDB single-table design: agents write multi-table schemas because they're easier to explain; force the single-table pattern with access-pattern enumeration.
- Cassandra/Scylla: agents accept "use them for analytics" — wrong, they're write-optimized OLTP/time-series; analytics needs ClickHouse or Spark.
- pgvector recall: agents quote IVFFlat recall numbers without tuning `lists` and `probes`; verify with real data.
- "Eventually consistent is fine" — agents accept this for shopping carts and inventory, leading to oversells. Force a per-operation consistency requirement.
- Backup, PITR, and DR: agents ignore them in cost models. Always include them; they often double the cost.
- Multi-tenant data isolation (schema per tenant vs row-level security vs DB per tenant) is missed; if app is SaaS, demand explicit choice.
- Vendor lock-in: managed services (DynamoDB, Spanner) lock data and surrounding ecosystem; agent must list the lock-in cost and switching plan.

## References
- DB-Engines Ranking — https://db-engines.com/en/ranking
- Martin Kleppmann, "Designing Data-Intensive Applications" (2017).
- Daniel Abadi, "Consistency Tradeoffs in Modern Distributed Database System Design" (PACELC).
- AWS DynamoDB Single-Table Design — https://www.alexdebrie.com/posts/dynamodb-single-table/
- pgvector docs — https://github.com/pgvector/pgvector
- Vector DB Bench — https://github.com/zilliztech/VectorDBBench
- "Choose the Right Database" (Microsoft Architecture Center) — https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-store-decision-tree
- TimescaleDB vs InfluxDB vs ClickHouse benchmarks — https://www.timescale.com/blog/tag/benchmarks/
