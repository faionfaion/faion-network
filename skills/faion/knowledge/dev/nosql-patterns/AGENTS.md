# NoSQL Patterns

## Summary

**One-sentence:** Data-modelling spec for document (MongoDB), key-value (Redis), wide-column (Cassandra), and graph (Neo4j) stores; access-pattern first, TTL on every cache key, partition keys frozen at design.

**One-paragraph:** Most NoSQL pain comes from modelling for entities instead of for access patterns, unbounded embedded arrays, missing TTLs, and partition keys that lock the team out of future queries. This methodology produces a typed data-model spec naming the store class, embed-vs-reference verdicts with cardinality evidence, partition-key choice with the primary access query, TTL policy per Redis prefix, and an index list per MongoDB collection. The spec ships before any collection is created and is validated against a JSON Schema.

**Ефективно для:**

- Перший NoSQL store у проекті - потрібно зафіксувати модель доступу.
- Міграція heavy JSONB-таблиці в MongoDB або key-value кеш.
- Redis-кеш накопичує ключі без TTL - пора зафіксувати політику.
- Cassandra/DynamoDB вибрано і треба заморозити partition key до запуску.
- Neo4j прототип переходить в production - індекси й traversal patterns треба зафіксувати.

## Applies If (ALL must hold)

- Access patterns are documented (read/write QPS, latency budget, primary queries).
- Data shape is genuinely flexible per record OR access is single-aggregate / time-series / graph.
- One named owner for the data model (a single human signs off the spec).
- Backing store class is shortlisted to one of: document / key-value / wide-column / graph.

## Skip If (ANY kills it)

- Strong relational invariants required (financial ledger, inventory with multi-row transactions).
- Ad-hoc OLAP / BI is a hard requirement - start with Postgres + warehouse.
- Project is a throwaway prototype with no production users.
- Team is unfamiliar with the chosen store and Postgres JSONB covers the use case.
- Compliance forbids the store class (e.g. data residency rules block managed Mongo).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Access-pattern register | markdown / table of queries with QPS + latency | product + engineering |
| Cardinality estimates | rows-per-entity / array growth bounds | analytics / domain expert |
| Compliance constraints | list of restrictions (PII, residency, retention) | legal / security |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[database-design]] | upstream relational baseline; spec inherits its access-pattern register format. |
| [[caching-strategy]] | consumer of the Redis-prefix + TTL section of this spec. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example for MongoDB + Redis | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-store-class` | sonnet | Score document / key-value / wide-column / graph on access patterns. |
| `draft-embed-vs-reference` | sonnet | Cardinality + read-frequency judgement. |
| `partition-key-design` | opus | Stakes high - choice is immutable at scale. |
| `ttl-policy` | haiku | Mechanical mapping prefix → ttl_seconds. |
| `index-list` | sonnet | Match indexes to query predicates. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nosql-data-model.json` | JSON skeleton for the data-model spec artefact. |
| `templates/redis-ttl-policy.yaml` | Prefix → TTL policy template. |
| `templates/nosql_picker.py` | Heuristic access-pattern → store class picker (CLI helper for the spec author). |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-nosql-patterns.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[database-design]]
- [[caching-strategy]]
- [[sql-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs — relational invariants needed?, access-pattern shape, expected partition skew, AI-tagging requirements — onto one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, picks the store class, and surfaces the partition-key decision early.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/nosql-data-model.json`

```json
{
  "store_class": "document",
  "access_patterns": [
    {
      "name": "get_entity_by_id",
      "qps": 0,
      "latency_ms_p95": 0
    }
  ],
  "model": {
    "entities": [],
    "embed_or_reference": {}
  },
  "ttl_policy": [
    {
      "prefix": "service:entity",
      "ttl_seconds": 3600
    }
  ],
  "indexes": [
    {
      "collection_or_label": "entities",
      "fields": []
    }
  ],
  "partition_key": {
    "key": "",
    "primary_query": ""
  }
}
```

### `templates/redis-ttl-policy.yaml`

```yaml
version: 1
ttl_policy:
  - prefix: auth:session
    ttl_seconds: 3600
  - prefix: cache:user-profile
    ttl_seconds: 600
  - prefix: ratelimit:ip
    ttl_seconds: 60
```

### `templates/nosql_picker.py`

```python
Usage: python nosql_picker.py "user sessions with TTL"
       python nosql_picker.py "time series sensor data 1B rows"
"""
import sys

PATTERNS = [
    # (pattern keywords, recommended_store, rationale)
    ("session cache ttl",           "redis",    "in-memory + TTL native"),
    ("rate limit sliding window",   "redis",    "sorted sets are O(log N)"),
    ("leaderboard counter rank",    "redis",    "ZADD/ZINCRBY atomic"),
    ("event stream consumer group", "redis",    "XADD/XREADGROUP, no broker needed"),
    ("nested aggregate embed",      "mongodb",  "embed + index on hot fields"),
    ("flexible cms content schema", "mongodb",  "schema evolution, partial validate"),
    ("time series billion rows",    "cassandra","partition by (entity, day)"),
    ("audit log append only write", "cassandra","write-optimized LSM"),
    ("recommendation social graph", "neo4j",    "graph traversal beats recursive CTEs"),
    ("relational jsonb occasional", "postgres", "JSONB is good enough; default choice"),
    ("unknown access pattern",      "postgres", "defer NoSQL until pain is measured"),
]


def pick(query: str) -> list[tuple[str, str, str]]:
    q = query.lower()
    return [p for p in PATTERNS if any(w in q for w in p[0].split())]


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not query:
        print("Usage: python nosql_picker.py <access pattern description>")
        sys.exit(1)
    matches = pick(query)
    if not matches:
        print("No match — default: postgres (start here, migrate on measured pain)")
    else:
        for store, _, rationale in matches:
            print(f"{store:10s} | {rationale}")
```

### `templates/_smoke-test.json`

```json
{
  "store_class": "document",
  "access_patterns": [
    {
      "name": "get_user_profile_by_id",
      "qps": 1200,
      "latency_ms_p95": 30
    }
  ],
  "model": {
    "entities": [
      "user"
    ],
    "embed_or_reference": {
      "preferences": "embed",
      "orders": "reference"
    }
  },
  "ttl_policy": [
    {
      "prefix": "auth:session",
      "ttl_seconds": 3600
    }
  ],
  "indexes": [
    {
      "collection_or_label": "users",
      "fields": [
        "email"
      ]
    }
  ],
  "partition_key": {
    "key": "tenant_id",
    "primary_query": "list users where tenant_id=?"
  }
}
```
