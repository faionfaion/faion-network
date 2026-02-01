# Database Selection Guide

Comprehensive framework for choosing the right database in 2026.

## Database Categories

| Category | Use Case | Examples |
|----------|----------|----------|
| **Relational (SQL)** | ACID transactions, complex queries, joins | PostgreSQL, MySQL, SQLite |
| **NewSQL** | Distributed SQL, global scale, strong consistency | CockroachDB, TiDB, Google Spanner, YugabyteDB |
| **Document** | Flexible schema, nested data, horizontal scaling | MongoDB, DynamoDB, Firestore, CouchDB |
| **Key-Value** | Caching, sessions, simple lookups | Redis, Memcached, DynamoDB |
| **Time-Series** | Metrics, IoT, monitoring, financial data | TimescaleDB, InfluxDB, ClickHouse, QuestDB |
| **Graph** | Relationships, social networks, knowledge graphs | Neo4j, Amazon Neptune, Dgraph, NebulaGraph |
| **Vector** | AI/ML embeddings, semantic search, RAG | Qdrant, Weaviate, Pinecone, Milvus, pgvector |
| **Search** | Full-text search, autocomplete, faceting | Elasticsearch, Meilisearch, Algolia |
| **Wide-Column** | Large-scale analytics, time-series at scale | Cassandra, ScyllaDB, HBase |

---

## Selection Decision Tree

```
Q: What is the primary data access pattern?
    |
    +-- Complex SQL queries, joins, transactions
    |   |
    |   +-- Single region, moderate scale --> PostgreSQL / MySQL
    |   |
    |   +-- Global distribution, strong consistency --> CockroachDB / TiDB / Spanner
    |
    +-- Document-oriented, flexible schema
    |   |
    |   +-- AWS ecosystem --> DynamoDB
    |   |
    |   +-- Self-hosted / multi-cloud --> MongoDB
    |
    +-- Simple key-value lookups, caching
    |   --> Redis / Memcached
    |
    +-- Time-stamped data (metrics, logs, IoT)
    |   |
    |   +-- PostgreSQL ecosystem --> TimescaleDB
    |   |
    |   +-- High-frequency monitoring --> InfluxDB
    |   |
    |   +-- Historical analytics --> ClickHouse
    |   |
    |   +-- Maximum ingestion speed --> QuestDB
    |
    +-- Highly connected data (relationships)
    |   |
    |   +-- Developer productivity, Cypher --> Neo4j
    |   |
    |   +-- AWS native, RDF + property graphs --> Neptune
    |   |
    |   +-- GraphQL-first --> Dgraph
    |
    +-- Vector embeddings (AI/ML, RAG)
    |   |
    |   +-- Already using PostgreSQL --> pgvector
    |   |
    |   +-- Complex metadata filtering --> Qdrant
    |   |
    |   +-- Knowledge graph + vectors --> Weaviate
    |   |
    |   +-- Billion-scale, GPU acceleration --> Milvus
    |   |
    |   +-- Fully managed, no ops --> Pinecone
    |
    +-- Full-text search
        |
        +-- Enterprise search, logging --> Elasticsearch
        |
        +-- Fast, typo-tolerant --> Meilisearch
        |
        +-- SaaS, hosted --> Algolia
```

---

## CAP Theorem Guide

The CAP theorem states distributed systems can guarantee only 2 of 3 properties:

- **C (Consistency)**: All nodes see the same data simultaneously
- **A (Availability)**: System remains operational despite node failures
- **P (Partition Tolerance)**: System functions during network partitions

### CAP Classification

| Type | Guarantees | Sacrifice | Databases |
|------|------------|-----------|-----------|
| **CP** | Consistency + Partition Tolerance | Availability during partitions | MongoDB, CockroachDB, Google Spanner, HBase |
| **AP** | Availability + Partition Tolerance | Strong consistency (eventual) | Cassandra, DynamoDB, CouchDB, ScyllaDB |
| **CA** | Consistency + Availability | Partition tolerance | PostgreSQL (single-node), MySQL (single-node) |

### When to Choose

| Priority | Choose | Examples |
|----------|--------|----------|
| Data accuracy (finance, banking) | CP | CockroachDB, MongoDB (w/ majority writes) |
| Always online (social, streaming) | AP | Cassandra, DynamoDB |
| Single region, no partitions | CA | PostgreSQL, MySQL |

### PACELC Extension

Beyond CAP, consider PACELC: "If Partition, choose A or C; Else choose Latency or Consistency"

| Database | Partition Behavior | Normal Behavior |
|----------|-------------------|-----------------|
| PostgreSQL | CA (no partitions) | EC (latency over consistency) |
| Cassandra | PA (availability) | EL (latency) |
| MongoDB | PC (consistency) | EC (latency) |
| CockroachDB | PC (consistency) | EC (configurable) |

---

## Database Comparison Matrix

### Relational vs NewSQL

| Criteria | PostgreSQL | MySQL | CockroachDB | TiDB | Spanner |
|----------|------------|-------|-------------|------|---------|
| **Distribution** | Single-node + replicas | Single-node + replicas | Native distributed | Native distributed | Native distributed |
| **Consistency** | Strong (single-node) | Strong (single-node) | Strong (global) | Strong (global) | Strong (global) |
| **Protocol** | PostgreSQL | MySQL | PostgreSQL | MySQL | PostgreSQL-like |
| **HTAP** | Limited | Limited | OLTP | OLTP + OLAP | OLTP + OLAP |
| **Scale** | Vertical + read replicas | Vertical + read replicas | Horizontal | Horizontal | Horizontal |
| **Best For** | General purpose | Web apps, WordPress | Global OLTP, payments | MySQL replacement, HTAP | GCP, petabyte scale |

### Vector Databases (2026)

| Criteria | Qdrant | Weaviate | Pinecone | Milvus | pgvector |
|----------|--------|----------|----------|--------|----------|
| **Type** | Purpose-built | Knowledge graph + vectors | Fully managed | Distributed vector | PostgreSQL extension |
| **Language** | Rust | Go | Managed | Go/C++ | C |
| **Hybrid Search** | Native | Native | Native | Native | Manual |
| **Max Scale** | Billions | Billions | Billions | Billions | 10-100M |
| **Metadata Filtering** | Advanced | Advanced | Good | Advanced | SQL WHERE |
| **Self-hosted** | Yes (Docker/K8s) | Yes (Docker/K8s) | No | Yes | Yes |
| **Best For** | Complex filtering, RAG | Semantic + graph | Zero ops | Billion-scale, GPU | Existing PostgreSQL |

### Time-Series Databases

| Criteria | TimescaleDB | InfluxDB | ClickHouse | QuestDB |
|----------|-------------|----------|------------|---------|
| **Base** | PostgreSQL extension | Purpose-built | Columnar OLAP | Purpose-built |
| **Query Language** | SQL | InfluxQL / Flux / SQL (v3) | SQL | SQL |
| **Ingestion Speed** | 1.3M pts/sec | High | Very High | Fastest (6.5x Timescale) |
| **Analytics** | Good | Monitoring-focused | Excellent | Good |
| **Best For** | PostgreSQL ecosystem | Real-time monitoring | Historical analytics | High-speed ingestion |

### Graph Databases

| Criteria | Neo4j | Neptune | Dgraph |
|----------|-------|---------|--------|
| **Query Language** | Cypher | Gremlin + SPARQL | DQL (GraphQL-like) |
| **Cloud** | Aura (managed) | AWS native | Self-hosted / Cloud |
| **RDF Support** | No | Yes | No |
| **Scaling** | Fabric (distributed) | Horizontal reads | Predicate sharding |
| **Best For** | Developer productivity | AWS, RDF/SPARQL | GraphQL APIs |

---

## Cost Considerations

### Managed vs Self-Hosted

| Factor | Managed (RDS, Atlas, Aura) | Self-Hosted (EC2, K8s) |
|--------|---------------------------|------------------------|
| **Setup Time** | Minutes | Hours to days |
| **Ops Overhead** | Minimal | Significant |
| **Monthly Cost (small)** | $50-200 | $20-100 + DBA time |
| **Monthly Cost (large)** | $2,000-20,000+ | $500-5,000 + team |
| **Backups** | Automatic | Manual setup |
| **HA/Failover** | Built-in | DIY |
| **Best For** | Most teams | Large scale, cost-sensitive |

### AWS RDS Pricing Examples (2026)

| Instance | Engine | Single-AZ | Multi-AZ |
|----------|--------|-----------|----------|
| db.t4g.micro | PostgreSQL | ~$12/mo | ~$24/mo |
| db.m5.large | PostgreSQL | ~$140/mo | ~$280/mo |
| db.m5.large | SQL Server | ~$700/mo | ~$1,400/mo |

**Cost Optimization:**
- Reserved Instances: Up to 69% savings for 1-3 year terms
- Spot instances for dev/test: 50-90% savings
- Right-sizing: Monitor and adjust instance size

### Vector Database Pricing

| Service | Free Tier | Paid Starting |
|---------|-----------|---------------|
| Pinecone | 100K vectors | $70/mo (Starter) |
| Qdrant Cloud | 1GB | Pay-as-you-go |
| Weaviate Cloud | 14-day trial | $25/mo (Sandbox) |
| Milvus (Zilliz) | 5GB | Pay-as-you-go |
| pgvector | N/A (PostgreSQL) | PostgreSQL costs |

---

## Polyglot Persistence

Modern applications often use multiple databases for different needs:

```
Application Layer
        |
        +-- PostgreSQL (primary data, transactions)
        |
        +-- Redis (caching, sessions, rate limiting)
        |
        +-- Elasticsearch (full-text search)
        |
        +-- Qdrant (vector embeddings, RAG)
        |
        +-- ClickHouse (analytics, reporting)
```

### Smart Factory Pattern (Time-Series)

```
Sensors --> InfluxDB (real-time, sub-ms alerts)
               |
               v
            Kafka
               |
        +------+------+
        |             |
        v             v
   ClickHouse    TimescaleDB
   (analytics)   (transactional)
```

---

## Quick Selection Guide

| Scenario | Recommended Database |
|----------|---------------------|
| General-purpose web app | PostgreSQL |
| High-traffic web app (AWS) | Aurora PostgreSQL |
| Global fintech, payments | CockroachDB or Spanner |
| MySQL replacement with scale | TiDB |
| Flexible schema, rapid iteration | MongoDB |
| Caching, sessions | Redis |
| IoT metrics, monitoring | InfluxDB or TimescaleDB |
| Analytics, data warehouse | ClickHouse |
| Social network, recommendations | Neo4j |
| RAG, semantic search (small) | pgvector |
| RAG, semantic search (production) | Qdrant or Weaviate |
| RAG, billion-scale | Milvus |
| Full-text search | Elasticsearch or Meilisearch |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Database selection | opus | Complex requirements and trade-offs |
| Schema design | sonnet | Logical to physical transformation |
| Query optimization | haiku | Applying index and join patterns |
## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step selection checklist |
| [examples.md](examples.md) | Use case examples with database choices |
| [templates.md](templates.md) | Decision matrix templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for database discussions |

## External Resources

- [DB-Engines Ranking](https://db-engines.com/en/ranking)
- [CAP Theorem (Wikipedia)](https://en.wikipedia.org/wiki/CAP_theorem)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Redis Documentation](https://redis.io/docs/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
