# Agent Integration — NoSQL Patterns

## When to use
- Schema is genuinely flexible per record (event payloads, IoT readings, CMS blocks).
- Access patterns are denormalized reads of nested aggregates (one user → embedded prefs+addresses).
- Time-series workloads (sensor data, analytics events) where bucket pattern + TTL fit naturally.
- Graph-shaped data (recommendations, social, knowledge graphs) where Neo4j/Memgraph beat recursive CTEs.
- High write throughput per partition exceeds RDBMS comfort (>5k writes/sec sustained).
- Polyglot persistence: hot session data in Redis, cold archival in S3+DynamoDB, search in OpenSearch.

## When NOT to use
- Strong relational integrity required (financial ledgers, inventory with multi-row invariants).
- Complex ad-hoc queries / OLAP — use Postgres + DuckDB or a warehouse.
- Team is unfamiliar with chosen NoSQL store and project is small — Postgres JSONB covers 80% of use cases.
- Default choice "because microservices" — premature; start with Postgres until you measure pain.
- Reporting / BI is a hard requirement — most BI tools assume SQL.

## Where it fails / limitations
- MongoDB: 16MB doc limit, no transactions across shards in older versions; unbounded arrays kill perf.
- Redis: in-memory only by default; persistence (RDB/AOF) has tradeoffs; cluster has key-slot constraints (`{tag}` syntax).
- Cassandra: no JOINs, no secondary index without performance penalty; partition key choice is permanent.
- Neo4j: vertical scaling ceiling; community edition has no clustering; Cypher learning curve.
- DynamoDB: hot partition throttling; `BatchWriteItem` ≤25 items; query patterns must be designed up-front.
- Eventual consistency surprises engineers used to ACID — read-your-writes anomalies under load.
- Schema migration without DDL: hard to reason about, easy to leave orphan fields forever.
- Aggregations across documents are slow vs SQL `GROUP BY` — push to materialized views or read replicas.

## Agentic workflow
Drive NoSQL design as: (1) agent enumerates **access patterns** (not entities) from PRD, (2) selects store per pattern (table below), (3) sketches partition/sort key OR document shape OR Redis structure, (4) generates schema doc + index plan + sample queries, (5) human reviews partition key + denormalization choices before code. Treat NoSQL data modeling as architecture work — not an implementation detail. Embed expected query latency targets (p95 < X ms) in the doc.

### Recommended subagents
- `faion-software-architect-agent` — owns store selection + access-pattern matrix.
- `faion-api-agent` — generates query layer (repositories) once schema is approved.
- `faion-sdd-executor-agent` — implements migrations + indexes under SDD gates.

### Prompt pattern
```
Given feature spec at .product/features/<X>/spec.md, output an
"access patterns" table: {pattern_name, read|write, frequency, latency_target,
key_fields, store_recommendation (mongo|redis|cassandra|neo4j|postgres+jsonb),
rationale}. Stop. Wait for review.
```

```
For approved access patterns using MongoDB, draft collection schemas with:
embedding vs reference decision per relationship, required indexes (with
explain hint), TTL fields, schema validation ($jsonSchema). No code yet.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mongosh` | Mongo shell, `explain()`, profiler | bundled with MongoDB |
| `redis-cli` / `valkey-cli` | Inspect keys, MONITOR, SLOWLOG | apt install redis-tools |
| `cqlsh` | Cassandra CQL shell | pip install cqlsh |
| `cypher-shell` | Neo4j CLI | bundled with Neo4j |
| `aws dynamodb` | DynamoDB CRUD via AWS CLI | pip install awscli |
| `mongoimport` / `mongodump` | Bulk load + backup | bundled |
| `redis-rdb-tools` | Analyze RDB memory usage | pip install rdbtools |
| `nosqlbench` | Load test multiple NoSQL stores | https://nosqlbench.io |
| `prisma` | Schema-first ORM, supports Mongo + Postgres | npm i prisma |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| MongoDB Atlas | SaaS | yes (Atlas API + CLI) | Free 512MB tier; Atlas Search, Vector Search built-in. |
| Redis Cloud / Upstash | SaaS | yes (REST + RESP) | Serverless Redis; Upstash has per-request billing. |
| Valkey | OSS | yes | Linux Foundation Redis fork; faion-net runs `valkey-server` already. |
| AWS DynamoDB | SaaS | yes (boto3) | Single-table design; pay-per-request mode. |
| ScyllaDB Cloud | SaaS | yes | Cassandra-API-compatible, faster. |
| Neo4j Aura | SaaS | yes (drivers) | Free dev tier; vector index since 5.11. |
| Memgraph | OSS+SaaS | yes | In-memory graph, openCypher-compatible. |
| Couchbase Capella | SaaS | yes | SQL++ over JSON. |
| FaunaDB | SaaS | yes | ACID + multi-region; serverless. |
| Firestore | SaaS | yes | Best for mobile/Firebase stacks. |

## Templates & scripts
See `templates.md` for full schema templates. Inline access-pattern → store decision helper:

```python
# scripts/nosql_picker.py — quick heuristic, not a substitute for review
PATTERNS = [
    # (pattern, recommended_store, why)
    ("session/cache, TTL < 1h",          "redis",    "in-memory + TTL native"),
    ("rate limiter, sliding window",      "redis",    "sorted sets are O(log N)"),
    ("leaderboard / counters",            "redis",    "ZADD/ZINCRBY"),
    ("event stream with consumers",       "redis",    "XADD/XREADGROUP, no broker"),
    ("nested aggregate, 1 doc reads",     "mongodb",  "embed + index on hot fields"),
    ("flexible CMS content",              "mongodb",  "schema evolution, partial validate"),
    ("time series > 1B rows",             "cassandra","partition by (entity, day)"),
    ("audit log, append-only",            "cassandra","write-optimized LSM"),
    ("user + product + recommendation",   "neo4j",    "graph traversal beats joins"),
    ("relational + occasional JSON",      "postgres", "JSONB is good enough; default"),
    ("unknown access patterns",           "postgres", "defer NoSQL until pain measured"),
]

def pick(query: str) -> list[tuple[str, str, str]]:
    q = query.lower()
    return [p for p in PATTERNS if any(w in q for w in p[0].split())]

if __name__ == "__main__":
    import sys
    for row in pick(" ".join(sys.argv[1:])):
        print(f"{row[1]:10s} | {row[0]:30s} | {row[2]}")
```

## Best practices
- Document access patterns BEFORE picking a store — the patterns drive the choice, not vice versa.
- Always set TTL on cache/session keys; without TTL Redis becomes append-only memory.
- Mongo: enable `$jsonSchema` validation in production collections; loose schemas rot.
- Cassandra: model by query, one table per access pattern; storage cost is cheap, latency is not.
- Neo4j: index every property used in `MATCH` predicates; missing index = full scan.
- Use `explain()` / `EXPLAIN ANALYZE` on every new query class; commit explain output to the schema doc.
- Backup strategy per store: `mongodump`, AOF+RDB, `nodetool snapshot`, `neo4j-admin dump`.
- Avoid `$where` and JS-server-side execution in Mongo — security + perf nightmare.
- Pin driver versions; major-version driver upgrades change wire protocol behaviors silently.
- Test with prod-like data volume — NoSQL pathologies (hot partitions, skew) only appear at scale.

## AI-agent gotchas
- Agents asked "use NoSQL" default to MongoDB regardless of fit — force them to choose store via the access-pattern matrix.
- LLMs forget partition key immutability in Cassandra/Dynamo and propose schemas that "just need a quick migration" — Dynamo can't change PK without table copy.
- Generated Mongo queries often miss indexes; ensure agent runs `db.collection.getIndexes()` and proposes new ones explicitly.
- Agents copy ObjectIds across docs without `populate`/lookup, then "forget" how to fetch the join. Force them to specify embed-vs-ref upfront.
- Schemaless ≠ schema-free: agents drop validation thinking it's flexible, then bad data flows in. Require `$jsonSchema` from day one.
- Redis: agents use raw keys without namespace prefix → key collisions across services. Enforce `{service}:{entity}:{id}` convention in prompts.
- LLMs hallucinate Cypher functions (`shortestPath()` accepts inline path patterns; agents wrap in subqueries unnecessarily). Pin to Neo4j 5.x docs.
- Human-in-loop checkpoint: data model decisions (partition key, embedding boundary, denormalization) — non-reversible at scale, must be human-approved.
- Vector search via NoSQL (Mongo Atlas Vector Search, Redis Vector Sim) is rapidly evolving — agents reference outdated APIs; pin to current minor version docs.

## References
- MongoDB data modeling — https://www.mongodb.com/docs/manual/data-modeling/
- Redis data types tutorial — https://redis.io/docs/data-types/
- Cassandra DDL guide — https://cassandra.apache.org/doc/latest/cassandra/data_modeling/
- Neo4j Cypher manual — https://neo4j.com/docs/cypher-manual/current/
- AWS DynamoDB single-table design — https://www.alexdebrie.com/posts/dynamodb-single-table/
- "Designing data-intensive applications" (Kleppmann) — book, ch. 2-3, 5-7
- Atlas Vector Search — https://www.mongodb.com/products/platform/atlas-vector-search
