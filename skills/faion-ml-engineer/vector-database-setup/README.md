# Vector Database Setup

Guide for setting up, configuring, and deploying vector databases in production environments.

## Overview

This skill covers the operational aspects of vector databases: initial setup, configuration tuning, deployment patterns, and production readiness. For database comparison and selection, see [vector-databases](../vector-databases/README.md).

**Focus areas:**
- Database installation and initialization
- Configuration for different workloads
- Deployment patterns (Docker, Kubernetes, managed)
- Production hardening and security
- Scaling and high availability

---

## Quick Start Guide

### Development Setup

| Database | Quickest Path |
|----------|---------------|
| **Chroma** | `pip install chromadb` (in-memory) |
| **Qdrant** | `docker run -p 6333:6333 qdrant/qdrant` |
| **Weaviate** | `docker run -p 8080:8080 semitechnologies/weaviate` |
| **pgvector** | Enable extension on existing PostgreSQL |
| **Milvus** | Docker Compose with etcd + MinIO |
| **Pinecone** | Sign up, get API key, no infra needed |

### Production Setup

| Database | Recommended Deployment |
|----------|------------------------|
| **Qdrant** | Kubernetes StatefulSet or Qdrant Cloud |
| **Weaviate** | Kubernetes with Helm or Weaviate Cloud |
| **Milvus** | Kubernetes cluster or Zilliz Cloud |
| **pgvector** | Managed PostgreSQL (RDS, Cloud SQL) + extension |
| **Pinecone** | Serverless (fully managed) |

---

## Setup by Database

### Qdrant

**Docker (Development)**
```bash
docker run -d --name qdrant \
  -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest
```

**Key Configuration**
```yaml
# qdrant_config.yaml
storage:
  storage_path: /qdrant/storage
  snapshots_path: /qdrant/snapshots

service:
  http_port: 6333
  grpc_port: 6334
  max_request_size_mb: 32

hnsw_index:
  m: 16                    # Connections per node (16-64)
  ef_construct: 100        # Build quality (100-500)
  full_scan_threshold: 10000

quantization:
  scalar:
    type: int8
    quantile: 0.99
    always_ram: true       # Keep quantized vectors in RAM
```

**Production Recommendations**
- Enable TLS for all connections
- Configure API key authentication
- Use gRPC (port 6334) for better performance
- Enable quantization for memory efficiency
- Set up replication for high availability

### Weaviate

**Docker (Development)**
```bash
docker run -d --name weaviate \
  -p 8080:8080 -p 50051:50051 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -v weaviate_data:/var/lib/weaviate \
  semitechnologies/weaviate:latest
```

**Key Configuration**
```yaml
# Environment variables
QUERY_DEFAULTS_LIMIT: 25
PERSISTENCE_DATA_PATH: /var/lib/weaviate
DEFAULT_VECTORIZER_MODULE: none
ENABLE_MODULES: text2vec-openai,generative-openai
AUTHENTICATION_APIKEY_ENABLED: true
AUTHENTICATION_APIKEY_ALLOWED_KEYS: your-api-key
```

**Production Recommendations**
- Disable anonymous access
- Enable API key or OIDC authentication
- Configure modules based on needs
- Use Helm chart for Kubernetes deployment
- Set up multi-node cluster for HA

### Milvus

**Docker Compose (Development)**
```bash
# Download and run standalone
wget https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh
bash standalone_embed.sh start
```

**Key Configuration**
```yaml
# milvus.yaml
etcd:
  endpoints:
    - etcd:2379

minio:
  address: minio
  port: 9000

proxy:
  port: 19530

queryNode:
  enableDisk: true      # Enable disk-based indexing

log:
  level: info
```

**Production Recommendations**
- Use distributed mode for scale
- Configure tiered storage (hot/warm/cold)
- Set up Pulsar for message queue
- Monitor with Prometheus/Grafana
- Consider Zilliz Cloud for managed service

### pgvector

**Extension Setup**
```sql
-- Enable extension (PostgreSQL 14+)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(1536)
);

-- Create HNSW index (production)
CREATE INDEX ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

**Key Configuration**
```sql
-- Set search quality (higher = better recall, slower)
SET hnsw.ef_search = 100;

-- Set maintenance memory for index builds
SET maintenance_work_mem = '1GB';
```

**Production Recommendations**
- Use HNSW index (not IVFFlat) for production
- Create partial indexes for filtered queries
- Configure connection pooling (PgBouncer)
- Regular VACUUM ANALYZE after bulk inserts
- Monitor index size and rebuild periodically

### Pinecone

**Setup (No Infrastructure)**
```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-api-key")

# Create serverless index
pc.create_index(
    name="my-index",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1",
    ),
)
```

**Production Recommendations**
- Use namespaces for multi-tenancy
- Configure metadata indexes for filtering
- Monitor query units for cost optimization
- Set up alerts for latency spikes

### Chroma

**Local Development**
```python
import chromadb

# Persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)
```

**Production Note**: Chroma is primarily for prototyping. For production, migrate to Qdrant, Weaviate, or another production-grade database.

---

## Deployment Patterns

### Pattern 1: Single Node (Development/Small Scale)

```
[Application] --> [Vector DB Container]
                        |
                  [Persistent Volume]
```

**Use case**: Development, testing, < 1M vectors
**Pros**: Simple, low cost
**Cons**: No HA, limited scale

### Pattern 2: Managed Service

```
[Application] --> [Load Balancer] --> [Managed Vector DB]
                                            |
                                    [Managed Storage]
```

**Use case**: Production without DevOps resources
**Pros**: Zero ops, auto-scaling, HA included
**Cons**: Higher cost, vendor lock-in

### Pattern 3: Self-Hosted Kubernetes

```
                    [Ingress]
                       |
[Application] --> [Service] --> [StatefulSet]
                                  |   |   |
                              [Pod] [Pod] [Pod]
                                |     |     |
                              [PVC] [PVC] [PVC]
```

**Use case**: Production at scale, control requirements
**Pros**: Full control, cost-efficient at scale
**Cons**: Operational overhead

### Pattern 4: Hybrid (Read Replicas)

```
[Write Path] --> [Primary Node]
                      |
              [Replication]
                   /    \
[Read Path] --> [Replica] [Replica]
```

**Use case**: Read-heavy workloads
**Pros**: Scale reads independently
**Cons**: Replication lag, complexity

---

## Configuration Tuning

### Index Parameters

| Parameter | Effect | Recommendation |
|-----------|--------|----------------|
| **M** (HNSW) | Connections per node | 16 (default), 32-64 for high recall |
| **ef_construct** | Build quality | 100-200 for production |
| **ef_search** | Search quality | Start at 50, increase for recall |
| **nlist** (IVF) | Number of clusters | sqrt(n) to 4*sqrt(n) |
| **nprobe** (IVF) | Clusters to search | nlist/10 to nlist/4 |

### Memory Management

| Strategy | Memory Reduction | Impact |
|----------|------------------|--------|
| Scalar quantization (int8) | 4x | 1-2% recall loss |
| Product quantization (PQ) | 8-32x | 3-5% recall loss |
| Binary quantization | 32x | 5-10% recall loss |
| On-disk payload | Variable | Slower payload access |
| On-disk vectors | Significant | Slower search |

### Workload Profiles

**Read-Heavy (RAG, Search)**
```yaml
# Optimize for low latency reads
hnsw:
  ef_search: 100-200
  m: 32
quantization:
  enabled: true
  type: scalar
caching:
  query_cache: enabled
```

**Write-Heavy (Indexing Pipeline)**
```yaml
# Optimize for throughput
batch_size: 500
async_indexing: true
optimizers:
  indexing_threshold: 50000
  flush_interval_sec: 30
```

**Balanced**
```yaml
# Default settings with monitoring
hnsw:
  ef_search: 100
  m: 16
monitoring:
  latency_alerts: true
  throughput_alerts: true
```

---

## Security Hardening

### Authentication

| Database | Auth Methods |
|----------|--------------|
| Qdrant | API key, TLS client certs |
| Weaviate | API key, OIDC, anonymous |
| Milvus | Username/password, TLS |
| pgvector | PostgreSQL auth (md5, scram) |
| Pinecone | API key |

### Network Security

- [ ] TLS encryption for all connections
- [ ] Private VPC/network deployment
- [ ] IP allowlisting where supported
- [ ] Firewall rules limiting access
- [ ] Service mesh for K8s (Istio, Linkerd)

### Data Security

- [ ] Encryption at rest enabled
- [ ] Backup encryption
- [ ] Access audit logging
- [ ] Data retention policies
- [ ] PII handling procedures

---

## High Availability

### Replication Configurations

| Database | HA Approach |
|----------|-------------|
| **Qdrant** | Distributed mode with sharding |
| **Weaviate** | Multi-node cluster |
| **Milvus** | Distributed architecture |
| **pgvector** | PostgreSQL streaming replication |
| **Pinecone** | Built-in (managed) |

### Disaster Recovery

- **RPO** (Recovery Point Objective): How much data can you lose?
  - Sync replication: ~0 data loss
  - Async replication: Minutes of data loss
  - Daily backups: Up to 24 hours

- **RTO** (Recovery Time Objective): How fast must you recover?
  - Hot standby: Minutes
  - Warm standby: Hours
  - Cold backup: Hours to days

---

## Monitoring

### Key Metrics

| Metric | Warning | Critical |
|--------|---------|----------|
| Query latency p95 | > 100ms | > 500ms |
| Query latency p99 | > 200ms | > 1s |
| Error rate | > 0.1% | > 1% |
| Memory usage | > 70% | > 85% |
| Disk usage | > 70% | > 85% |
| Replication lag | > 1s | > 10s |

### Observability Stack

```
[Vector DB] --> [Prometheus] --> [Grafana]
      |              |
      +-------> [AlertManager] --> [PagerDuty/Slack]
```

---

## Cost Optimization

### Self-Hosted Strategies

1. **Right-size instances**: Start small, scale based on metrics
2. **Enable quantization**: 4-32x memory reduction
3. **Use spot/preemptible for non-critical**: 60-90% savings
4. **Tiered storage**: Move cold data to cheaper storage
5. **Reserved instances**: 30-60% savings for predictable workloads

### Managed Service Strategies

1. **Choose serverless when possible**: Pay per query
2. **Monitor query patterns**: Optimize hot paths
3. **Batch operations**: Reduce API calls
4. **Cache frequent queries**: Reduce database load
5. **Right-size dimensions**: Smaller embeddings = lower cost

---

## File Structure

```
vector-database-setup/
├── README.md           # This file - setup overview
├── checklist.md        # Setup and deployment checklists
├── examples.md         # Configuration and deployment examples
├── templates.md        # Docker, K8s, Terraform templates
└── llm-prompts.md      # Prompts for setup assistance
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [vector-databases](../vector-databases/README.md) | Database comparison and selection |
| [faion-rag-engineer](../../faion-rag-engineer/CLAUDE.md) | RAG pipeline integration |
| [faion-infrastructure-engineer](../../faion-infrastructure-engineer/CLAUDE.md) | Kubernetes, Docker deployment |

---


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Vector DB selection | sonnet | Tool evaluation |
| Schema design | sonnet | Data structure |
| Index configuration | sonnet | Performance tuning |

## Sources

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Milvus Documentation](https://milvus.io/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Best Vector Databases 2025](https://lakefs.io/blog/best-vector-databases/)
- [Vector Databases for RAG 2025](https://latenode.com/blog/ai-frameworks-technical-infrastructure/vector-databases-embeddings/best-vector-databases-for-rag-complete-2025-comparison-guide)

---

*Vector Database Setup v1.0*
*Part of faion-ml-engineer skill*
