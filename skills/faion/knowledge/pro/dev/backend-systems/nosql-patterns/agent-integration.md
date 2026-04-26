# Agent Integration — NoSQL Patterns

## When to use
- Modeling document/key-value/wide-column/graph stores from access patterns rather than entity diagrams.
- Migrating relational schemas to MongoDB, DynamoDB, Cassandra, or Neo4j when join cost dominates.
- Designing time-series, leaderboard, rate-limit, session, or feed schemas where Redis structures or Cassandra clustering keys are a natural fit.
- Polyglot persistence work where you need to pick the right NoSQL family per workload.

## When NOT to use
- Strong-consistency, multi-row transactional workloads (financial ledgers, inventory with reservations) — stay relational.
- Ad-hoc analytical queries with unknown access patterns — NoSQL design assumes you know the queries.
- Small datasets (<100 GB, low QPS) where Postgres + JSONB is simpler than running another engine.
- Reporting/BI surfaces — those belong on a warehouse/lakehouse, not the operational NoSQL store.

## Where it fails / limitations
- Document size caps (MongoDB 16 MB, DynamoDB 400 KB) — unbounded arrays / append-only embeds eventually break.
- Hot partitions in Cassandra/DynamoDB when partition key has low cardinality or skew (one tenant dominates writes).
- Eventual consistency surprises: read-after-write races, lost updates without conditional writes / `IF NOT EXISTS`.
- Secondary index limitations (DynamoDB GSI projection cost, Cassandra anti-patterns) push you to materialized views or duplicate tables.
- Graph queries that traverse many hops (>5) explode in cost on Neo4j without query shaping.

## Agentic workflow
Use a planning pass with Opus to enumerate access patterns and pick the NoSQL family before any code is written, then hand the schema design to a coding subagent (Sonnet) that emits index definitions, migration scripts, and repository code in one batch. Treat schema as a deliverable file (committed alongside code) so the next agent can diff it. Always run a load-shape sanity check (estimated docs/s, partition cardinality, hottest key) as a separate review step before merging.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the SDD task (spec → design → impl → review) for a NoSQL schema change with quality gates.
- A custom `nosql-schema-reviewer` (Opus) — read-only auditor that scores a proposed schema against the documented access-pattern list and flags hot-partition / unbounded-array smells before merge.
- `password-scrubber-agent` — sanitize connection strings / credentials in any committed schema or migration scripts.

### Prompt pattern
```
You are designing a <MongoDB|DynamoDB|Cassandra|Neo4j|Redis> schema.
Inputs: (1) list of access patterns with QPS estimates, (2) entity sketch, (3) consistency requirements.
Output a single Markdown file with: collection/table list, partition+sort/clustering keys, indexes, sample documents, write paths, invalidation rules, and one anti-pattern check per table.
Do NOT propose joins. Model for queries.
```

```
Audit the attached schema against knowledge/pro/dev/backend-systems/nosql-patterns/README.md anti-patterns.
Return: {hot_partitions[], unbounded_arrays[], missing_indexes[], consistency_risks[], score 0-100}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mongosh` | MongoDB shell, indexes, explain | https://www.mongodb.com/docs/mongodb-shell/ |
| `mongodump` / `mongorestore` | Backups, schema migration cutover | https://www.mongodb.com/docs/database-tools/ |
| `redis-cli` | Inspect keys, MEMORY USAGE, latency monitor | https://redis.io/docs/connect/cli/ |
| `aws dynamodb` | Table mgmt, partition stats, on-demand backups | https://docs.aws.amazon.com/cli/latest/reference/dynamodb/ |
| `cqlsh` | Cassandra/ScyllaDB shell, tracing, prepared stmts | https://cassandra.apache.org/doc/latest/cassandra/tools/cqlsh.html |
| `cypher-shell` | Neo4j queries, EXPLAIN/PROFILE | https://neo4j.com/docs/operations-manual/current/tools/cypher-shell/ |
| `migrate` (golang-migrate) | Versioned migrations incl. Mongo, Cassandra | https://github.com/golang-migrate/migrate |
| `kcat` (ex-kafkacat) | Useful when NoSQL fed by Kafka CDC | https://github.com/edenhill/kcat |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| MongoDB Atlas | SaaS | Yes | Atlas Admin API + `mongosh`; agents can create indexes/clusters via REST. |
| DynamoDB | SaaS (AWS) | Yes | Drive via `aws dynamodb` or boto3; NoSQL Workbench produces JSON models the agent can consume. |
| Amazon Keyspaces | SaaS | Partial | Cassandra wire protocol; some DDL differs — agents must check feature matrix. |
| ScyllaDB Cloud | SaaS | Yes | CQL-compatible, REST mgmt API; better for high-throughput. |
| Redis Cloud / ElastiCache | SaaS | Yes | All commands via `redis-cli`; Streams/Search/JSON modules expand patterns. |
| Neo4j AuraDB | SaaS | Yes | Bolt + HTTP API; `cypher-shell` non-interactive mode is agent-friendly. |
| Cassandra (self-host) | OSS | Yes | `cqlsh -e`, nodetool; require operator agent to handle compaction tuning. |
| FerretDB | OSS | Yes | Mongo wire protocol over Postgres — useful when agent wants Mongo API on existing Postgres. |

## Templates & scripts
See `templates.md` and `examples.md` for full Mongo/Redis/Cassandra/Neo4j snippets. Inline helper for partition-key sanity check (Cassandra/DynamoDB):

```python
# scripts/partition_sanity.py
# Reads a CSV of (partition_key, write_count) and flags skew / unbounded growth.
import csv, statistics, sys
rows = [(r[0], int(r[1])) for r in csv.reader(open(sys.argv[1]))]
counts = [c for _, c in rows]
mean, p99 = statistics.mean(counts), statistics.quantiles(counts, n=100)[98]
hot = [(k, c) for k, c in rows if c > 10 * mean]
print(f"keys={len(rows)} mean={mean:.1f} p99={p99} hot_keys={len(hot)}")
for k, c in sorted(hot, key=lambda x: -x[1])[:10]:
    print(f"  HOT {k}: {c} writes ({c/mean:.1f}x mean)")
```

## Best practices
- Write the access-pattern list (query, filters, sort, QPS, latency budget) BEFORE choosing the NoSQL family — this artifact is the single most useful agent input.
- Encode invalidation/TTL rules next to the schema (`createIndex({...}, {expireAfterSeconds})`, DynamoDB TTL attribute) — agents forget cleanup otherwise.
- For Mongo, default to a `schemaVersion` field on every document; agents that emit migrations must bump it and write a forward+backward script.
- Use conditional writes (`updateOne` with filter, DynamoDB `ConditionExpression`, Cassandra LWT) anywhere the agent reasons "read-then-write" — eventual consistency will bite otherwise.
- Cap embedded arrays explicitly (`$slice`, bucket pattern) and document the cap in the schema file; agents tend to embed unboundedly.
- For Redis, always set `EXPIRE` or use a key-namespacing convention the agent can sweep; otherwise leaks accumulate silently.

## AI-agent gotchas
- LLMs default to relational thinking and propose joins / cross-collection lookups — explicitly forbid joins in the system prompt and require denormalization rationale per duplicated field.
- Agents pick PRIMARY KEY based on entity ID, not query — require them to cite which access pattern justifies the partition+clustering key choice.
- Mongo `_id` defaults to ObjectId; agents often overwrite it with a string and lose insertion-order locality. Make this an explicit checklist item.
- Agents over-trust eventual consistency for "small" updates (counters, balances). Force them to flag any read-modify-write and route it through atomic ops (`$inc`, `HINCRBY`, `UpdateItem` with `ADD`).
- Cassandra `ALLOW FILTERING` and Mongo `$where` are red flags — block them in code review prompts.
- Human-in-loop checkpoint: schema approval before any migration script runs in a non-dev env. Agent must produce dry-run output (estimated docs touched, index build time) and wait for `/approve` before executing.

## References
- MongoDB data modeling guide — https://www.mongodb.com/docs/manual/data-modeling/
- DynamoDB best practices — https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html
- Cassandra data modeling — https://cassandra.apache.org/doc/latest/cassandra/data_modeling/
- Redis patterns — https://redis.io/docs/manual/patterns/
- Neo4j graph data modeling — https://neo4j.com/docs/getting-started/data-modeling/
- "Designing Data-Intensive Applications" (Kleppmann) — chapters 2, 5, 7.
