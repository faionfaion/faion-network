# Database Selection

Framework for choosing the right database.

## Decision Tree

```
Q: What is the primary data pattern?
    │
    ├─ Complex queries, joins, transactions
    │   → Relational (PostgreSQL, MySQL)
    │
    ├─ Document-oriented, flexible schema
    │   → Document DB (MongoDB, DynamoDB)
    │
    ├─ Simple key-value lookups
    │   → Key-Value (Redis, DynamoDB)
    │
    ├─ Time-series data (metrics, logs)
    │   → Time-Series (TimescaleDB, InfluxDB)
    │
    ├─ Highly connected data (graphs)
    │   → Graph DB (Neo4j, Neptune)
    │
    └─ Full-text search
        → Search (Elasticsearch, Meilisearch)
```

## Database Types

### Relational (SQL)

| Database | Best For |
|----------|----------|
| **PostgreSQL** | General purpose, JSONB, extensions |
| **MySQL** | Web apps, WordPress, simple OLTP |
| **SQLite** | Embedded, mobile, small apps |
| **CockroachDB** | Distributed SQL, global scale |

**Choose when:**
- ACID transactions required
- Complex queries with joins
- Data integrity critical
- Schema is relatively stable

### Document (NoSQL)

| Database | Best For |
|----------|----------|
| **MongoDB** | Flexible schema, JSON documents |
| **DynamoDB** | Serverless, AWS native, key-value + document |
| **Firestore** | Real-time, mobile/web sync |
| **CouchDB** | Offline-first, sync |

**Choose when:**
- Schema evolves frequently
- Nested/hierarchical data
- Horizontal scaling priority
- Document-oriented access patterns

### Key-Value

| Database | Best For |
|----------|----------|
| **Redis** | Caching, sessions, pub/sub, leaderboards |
| **Memcached** | Simple caching |
| **DynamoDB** | Serverless key-value |

**Choose when:**
- Simple lookups by key
- Caching layer
- Session storage
- Real-time counters

### Time-Series

| Database | Best For |
|----------|----------|
| **TimescaleDB** | PostgreSQL extension, SQL queries |
| **InfluxDB** | Metrics, IoT, monitoring |
| **ClickHouse** | Analytics, OLAP |

**Choose when:**
- Metrics, monitoring data
- IoT sensor data
- Financial tick data
- Log aggregation

### Graph

| Database | Best For |
|----------|----------|
| **Neo4j** | Social networks, recommendations |
| **Amazon Neptune** | AWS managed graph |
| **Dgraph** | Distributed graph |

**Choose when:**
- Social networks
- Recommendation engines
- Fraud detection
- Knowledge graphs

### Search

| Database | Best For |
|----------|----------|
| **Elasticsearch** | Full-text search, logging |
| **Meilisearch** | Fast search, typo-tolerant |
| **Algolia** | Hosted search (SaaS) |

**Choose when:**
- Full-text search
- Autocomplete
- Faceted navigation
- Log analysis (ELK)

## Comparison Matrix

| Criteria | PostgreSQL | MongoDB | Redis | Elasticsearch |
|----------|------------|---------|-------|---------------|
| Consistency | Strong | Configurable | Strong | Eventual |
| Scale writes | Moderate | High | Very High | High |
| Scale reads | High (replicas) | High | Very High | Very High |
| Joins | Excellent | Limited | None | Limited |
| Schema | Fixed | Flexible | None | Flexible |
| Transactions | ACID | Multi-doc ACID | Limited | None |

## Polyglot Persistence

Use different databases for different needs:

```
┌─────────────────────────────────────────────┐
│                Application                   │
├─────────────────────────────────────────────┤
│                                             │
│  PostgreSQL     Redis      Elasticsearch    │
│  (main data)    (cache)    (search)         │
│                                             │
└─────────────────────────────────────────────┘
```

## Scalability Considerations

### Vertical Scaling (Scale Up)
- Bigger machine
- Works for most databases
- Has limits

### Horizontal Scaling (Scale Out)

| Strategy | Description | Databases |
|----------|-------------|-----------|
| Read replicas | Copy data to read-only nodes | PostgreSQL, MySQL |
| Sharding | Partition data across nodes | MongoDB, CockroachDB |
| Clustering | Distributed nodes | Redis Cluster, Cassandra |

## Managed vs Self-Hosted

| Managed | Self-Hosted |
|---------|-------------|
| AWS RDS, Cloud SQL | Own servers |
| Less ops overhead | Full control |
| Higher cost at scale | Lower cost, more work |
| Automatic backups | Manual setup |

## Decision Checklist

```markdown
[ ] Data model: Relational? Document? Graph?
[ ] Query patterns: Complex joins? Simple lookups?
[ ] Consistency: Strong ACID? Eventual OK?
[ ] Scale: Read-heavy? Write-heavy? Both?
[ ] Team expertise: What do we know?
[ ] Ecosystem: Tooling, community, support?
[ ] Cost: License, infrastructure, ops?
[ ] Managed option available?
```

## Related

- [data-modeling.md](data-modeling.md) - Schema design
- [caching-architecture.md](caching-architecture.md) - Caching layer
