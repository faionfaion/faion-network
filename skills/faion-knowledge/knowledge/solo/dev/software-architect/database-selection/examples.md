# Database Selection Examples

Real-world use cases with database selection rationale.

---

## E-Commerce Platform

### Requirements
- Product catalog with complex attributes
- User accounts and order history
- Shopping cart and checkout
- Search with filters and autocomplete
- Personalized recommendations
- Order analytics

### Database Selection

| Component | Database | Rationale |
|-----------|----------|-----------|
| Core data | PostgreSQL | ACID for orders, rich SQL for catalog |
| Sessions/Cart | Redis | Fast reads, TTL expiration |
| Search | Elasticsearch | Full-text, faceted filters |
| Recommendations | Neo4j | Product-user relationships |
| Analytics | ClickHouse | Historical order analysis |

### Architecture

```
User Request
     |
     v
  API Layer
     |
     +-- PostgreSQL (products, orders, users)
     |
     +-- Redis (sessions, cart, rate limiting)
     |
     +-- Elasticsearch (product search, autocomplete)
     |
     +-- Neo4j (recommendations: "users who bought X also bought Y")
     |
     +-- ClickHouse (sales analytics, reporting)
```

### Key Decisions
- **Why PostgreSQL over MongoDB?** Strong ACID for payment transactions, complex product queries with joins
- **Why Elasticsearch over PostgreSQL full-text?** Superior relevance ranking, faceted navigation, typo tolerance
- **Why separate analytics DB?** ClickHouse handles 100x better for aggregations without impacting OLTP

---

## SaaS Application (Multi-Tenant)

### Requirements
- Multi-tenant data isolation
- User authentication and authorization
- Real-time collaboration features
- API rate limiting
- Usage analytics per tenant
- Full-text search within tenant

### Database Selection

| Component | Database | Rationale |
|-----------|----------|-----------|
| Core data | PostgreSQL | Row-level security, mature multi-tenant patterns |
| Cache/Sessions | Redis | Rate limiting, real-time pub/sub |
| Search | Meilisearch | Per-tenant indexing, fast, easy to manage |
| Usage metrics | TimescaleDB | Time-series with PostgreSQL ecosystem |

### Multi-Tenancy Pattern

```sql
-- PostgreSQL Row-Level Security
CREATE POLICY tenant_isolation ON all_tables
  USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- TimescaleDB for usage metrics
CREATE TABLE usage_metrics (
  time TIMESTAMPTZ NOT NULL,
  tenant_id UUID NOT NULL,
  metric_name TEXT,
  value NUMERIC
);
SELECT create_hypertable('usage_metrics', 'time');
```

### Key Decisions
- **Why PostgreSQL over CockroachDB?** Single-region deployment, PostgreSQL expertise, cost-effective
- **Why Meilisearch over Elasticsearch?** Simpler ops, faster for small-medium datasets, per-tenant isolation easier
- **Why TimescaleDB?** Unified PostgreSQL ecosystem, SQL for metrics queries

---

## RAG-Based AI Application

### Requirements
- Store document embeddings (1536 dimensions)
- Semantic search over 10M+ documents
- Metadata filtering (date, source, category)
- Hybrid search (semantic + keyword)
- Document storage and retrieval
- Chat history persistence

### Database Selection

| Component | Database | Rationale |
|-----------|----------|-----------|
| Embeddings | Qdrant | Advanced filtering, high performance |
| Documents | PostgreSQL | JSONB for flexible document storage |
| Chat history | PostgreSQL | Relational structure, easy queries |
| Cache | Redis | LLM response caching |

### Architecture

```
User Query
     |
     v
  Embedding Model (OpenAI/Claude)
     |
     v
  Qdrant (semantic search)
     |
     +-- Returns: doc_ids, scores
     |
     v
  PostgreSQL (fetch full documents)
     |
     v
  LLM (generate response)
     |
     v
  Redis (cache response)
```

### Qdrant Configuration

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient("localhost", port=6333)

# Create collection with optimized settings
client.create_collection(
    collection_name="documents",
    vectors_config=models.VectorParams(
        size=1536,  # OpenAI embedding dimension
        distance=models.Distance.COSINE
    ),
    optimizers_config=models.OptimizersConfigDiff(
        indexing_threshold=20000
    )
)

# Search with metadata filtering
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="technical")
            ),
            models.FieldCondition(
                key="date",
                range=models.Range(gte="2024-01-01")
            )
        ]
    ),
    limit=10
)
```

### Key Decisions
- **Why Qdrant over pgvector?** Better performance at 10M+ vectors, advanced filtering
- **Why Qdrant over Pinecone?** Self-hosted option, no vendor lock-in, cost control
- **Why PostgreSQL for documents?** Reliable storage, JSONB flexibility, backup ecosystem

---

## IoT Platform

### Requirements
- Ingest 1M+ events per second
- Store 1+ year of sensor data
- Real-time alerting (sub-second)
- Historical analytics and dashboards
- Device management
- Multi-tenant (customer isolation)

### Database Selection

| Component | Database | Rationale |
|-----------|----------|-----------|
| Real-time metrics | InfluxDB | Optimized for high-frequency ingestion |
| Historical analytics | ClickHouse | Fast aggregations, columnar storage |
| Device management | PostgreSQL | ACID for device configuration |
| Alert state | Redis | Fast reads for threshold checking |

### Architecture (Smart Factory Pattern)

```
Sensors --> Kafka --> InfluxDB (real-time, 7-day retention)
                          |
                          v
                    Alert Engine (Redis for state)
                          |
                          v
            ClickHouse (historical, 1+ year retention)
                          |
                          v
                    Grafana Dashboards
```

### Data Flow

1. **Hot data (0-7 days)**: InfluxDB for real-time queries and alerts
2. **Warm data (7-90 days)**: ClickHouse for dashboards and analysis
3. **Cold data (90+ days)**: ClickHouse with compression, S3 for raw data

### Key Decisions
- **Why InfluxDB + ClickHouse?** Different strengths: InfluxDB for real-time, ClickHouse for analytics
- **Why not just TimescaleDB?** Higher ingestion rate needed, analytics query patterns favor columnar
- **Why Kafka in between?** Decouples ingestion from processing, replay capability

---

## Global Fintech Application

### Requirements
- Distributed across 3+ regions
- Strong consistency for transactions
- Sub-100ms latency globally
- Regulatory compliance (PCI-DSS)
- High availability (99.99%)
- Audit logging

### Database Selection

| Component | Database | Rationale |
|-----------|----------|-----------|
| Transactions | CockroachDB | Distributed ACID, PostgreSQL compatible |
| Cache | Redis Cluster | Global cache, low latency |
| Audit logs | ClickHouse | Append-only, fast queries |
| Search (compliance) | Elasticsearch | Full-text search for KYC/AML |

### CockroachDB Configuration

```sql
-- Multi-region table with zone constraints
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    amount DECIMAL(19,4) NOT NULL,
    currency CHAR(3) NOT NULL,
    region STRING NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
) LOCALITY REGIONAL BY ROW AS region;

-- Pin data to specific regions for compliance
ALTER TABLE transactions CONFIGURE ZONE USING
    constraints = '[+region=eu-west-1]',
    lease_preferences = '[[+region=eu-west-1]]';
```

### Key Decisions
- **Why CockroachDB over Spanner?** Multi-cloud flexibility, PostgreSQL compatibility
- **Why not TiDB?** CockroachDB's stronger consistency guarantees for financial transactions
- **Why Redis Cluster?** Global cache distribution, consistent hashing

---

## Social Network / Content Platform

### Requirements
- User profiles and connections
- Content feed generation
- Real-time notifications
- Message threading
- Full-text search
- Analytics

### Database Selection

| Component | Database | Rationale |
|-----------|----------|-----------|
| User/Post data | PostgreSQL | Core relational data |
| Social graph | Neo4j | Friend relationships, recommendations |
| Feed cache | Redis | Precomputed feeds, fast reads |
| Notifications | Redis Streams | Real-time push |
| Search | Elasticsearch | User/content search |
| Messages | ScyllaDB | High write throughput, AP model |

### Feed Generation Pattern

```
User posts content
        |
        v
PostgreSQL (store post)
        |
        v
Kafka (fan-out event)
        |
        +-- Neo4j (update graph, find followers)
        |
        +-- Redis (update follower feeds)
        |
        +-- Elasticsearch (index for search)
```

### Key Decisions
- **Why Neo4j for graph?** Efficient friend-of-friend queries, recommendation algorithms
- **Why ScyllaDB for messages?** High write throughput, eventual consistency acceptable for messages
- **Why Redis for feeds?** Pre-computed feeds, sub-millisecond reads

---

## Startup MVP (Cost-Optimized)

### Requirements
- Rapid development
- Minimal ops overhead
- Low initial cost
- Room to scale later
- Single-region deployment

### Database Selection

| Component | Database | Rationale |
|-----------|----------|-----------|
| Everything | PostgreSQL + extensions | Single database, max simplicity |

### PostgreSQL as Multi-Purpose

```sql
-- Relational data
CREATE TABLE users (...);
CREATE TABLE orders (...);

-- Document storage (JSONB)
CREATE TABLE events (
    id UUID PRIMARY KEY,
    data JSONB NOT NULL
);

-- Full-text search
CREATE INDEX idx_products_search ON products
    USING GIN (to_tsvector('english', name || ' ' || description));

-- Vector search (pgvector)
CREATE EXTENSION vector;
CREATE TABLE embeddings (
    id UUID PRIMARY KEY,
    embedding vector(1536)
);

-- Time-series (basic)
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    metric TEXT,
    value NUMERIC
);
CREATE INDEX idx_metrics_time ON metrics (time DESC);
```

### Migration Path

As the startup grows:
1. **Phase 1 (MVP)**: PostgreSQL only
2. **Phase 2 (Growth)**: Add Redis for caching
3. **Phase 3 (Scale)**: Migrate search to Elasticsearch/Meilisearch
4. **Phase 4 (Maturity)**: Migrate vectors to Qdrant, time-series to TimescaleDB

### Key Decisions
- **Why PostgreSQL for MVP?** Single database to manage, rich extensions, easy to hire for
- **When to split?** When specific workload needs dedicated optimization

---

## Summary: Database by Use Case

| Use Case | Primary Database | Supporting Databases |
|----------|-----------------|---------------------|
| E-commerce | PostgreSQL | Redis, Elasticsearch, Neo4j |
| SaaS multi-tenant | PostgreSQL | Redis, Meilisearch, TimescaleDB |
| RAG/AI application | Qdrant/Weaviate | PostgreSQL, Redis |
| IoT platform | InfluxDB | ClickHouse, PostgreSQL, Redis |
| Global fintech | CockroachDB | Redis Cluster, ClickHouse |
| Social network | PostgreSQL | Neo4j, Redis, ScyllaDB |
| Startup MVP | PostgreSQL | (add others as needed) |

---

## Related

- [README.md](README.md) - Database categories overview
- [checklist.md](checklist.md) - Selection checklist
- [templates.md](templates.md) - Decision matrix templates
- [llm-prompts.md](llm-prompts.md) - AI-assisted selection
