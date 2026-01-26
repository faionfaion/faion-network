# Vector Database Checklists

Comprehensive checklists for database selection, setup, performance tuning, and production readiness.

---

## Database Selection Checklist

### Requirements Gathering

- [ ] **Data characteristics**
  - [ ] Expected number of vectors (current and 12-month projection)
  - [ ] Vector dimensions (768, 1024, 1536, 3072)
  - [ ] Metadata fields and their types
  - [ ] Update frequency (real-time, batch, rarely)
  - [ ] Delete/update requirements

- [ ] **Query patterns**
  - [ ] Expected queries per second (QPS)
  - [ ] Latency requirements (p50, p95, p99)
  - [ ] Recall requirements (90%, 95%, 99%)
  - [ ] Filter complexity (simple, moderate, complex)
  - [ ] Hybrid search needs (keyword + vector)

- [ ] **Infrastructure constraints**
  - [ ] Cloud vs self-hosted preference
  - [ ] Existing infrastructure (PostgreSQL, Kubernetes)
  - [ ] Team expertise (DevOps capabilities)
  - [ ] Budget constraints
  - [ ] Compliance requirements (SOC2, HIPAA, GDPR)

### Evaluation Matrix

| Criterion | Weight | Qdrant | Weaviate | Milvus | Pinecone | pgvector | Chroma |
|-----------|--------|--------|----------|--------|----------|----------|--------|
| Scale (vectors) | | | | | | | |
| Latency | | | | | | | |
| Throughput | | | | | | | |
| Filtering | | | | | | | |
| Hybrid search | | | | | | | |
| Ops complexity | | | | | | | |
| Cost | | | | | | | |
| **Total Score** | | | | | | | |

### Decision Validation

- [ ] Proof of concept completed with representative data
- [ ] Benchmarked with expected query patterns
- [ ] Validated filtering performance
- [ ] Tested failure scenarios (node restart, network partition)
- [ ] Estimated monthly cost at projected scale
- [ ] Reviewed vendor roadmap and community health
- [ ] Confirmed SDK availability for tech stack

---

## Setup & Configuration Checklist

### Qdrant Setup

- [ ] **Installation**
  - [ ] Docker image pulled (`qdrant/qdrant:latest`)
  - [ ] Ports configured (6333 HTTP, 6334 gRPC)
  - [ ] Storage volume mounted
  - [ ] Memory limits set appropriately

- [ ] **Collection configuration**
  - [ ] Vector size matches embedding model
  - [ ] Distance metric selected (Cosine, Dot, Euclidean)
  - [ ] HNSW parameters tuned (m, ef_construct)
  - [ ] On-disk payload enabled for large payloads
  - [ ] Quantization configured if needed

- [ ] **Payload indexes**
  - [ ] Keyword indexes for categorical filters
  - [ ] Integer indexes for numeric range queries
  - [ ] DateTime indexes for temporal filters
  - [ ] Text indexes for full-text search (if needed)

- [ ] **Security**
  - [ ] API key configured
  - [ ] TLS enabled for production
  - [ ] Network policies set (firewall rules)

### Weaviate Setup

- [ ] **Installation**
  - [ ] Docker image or Helm chart deployed
  - [ ] Persistence volume configured
  - [ ] Module selection (text2vec, etc.)

- [ ] **Schema design**
  - [ ] Classes defined with properties
  - [ ] Data types specified for each property
  - [ ] Vectorizer configured (or none for BYOV)
  - [ ] Cross-references defined if needed

- [ ] **Index configuration**
  - [ ] HNSW parameters set
  - [ ] Distance metric selected
  - [ ] Inverted index enabled for filtering

- [ ] **Authentication**
  - [ ] Anonymous access disabled for production
  - [ ] API key or OIDC configured

### Milvus Setup

- [ ] **Installation**
  - [ ] Deployment mode selected (standalone, cluster)
  - [ ] etcd, MinIO, Pulsar configured (for cluster)
  - [ ] Resource limits set

- [ ] **Collection configuration**
  - [ ] Schema defined with field types
  - [ ] Vector field configured
  - [ ] Primary key field set
  - [ ] Partition strategy planned

- [ ] **Index creation**
  - [ ] Index type selected (HNSW, IVF_FLAT, etc.)
  - [ ] Index parameters configured
  - [ ] Index built after data load

- [ ] **Consistency level**
  - [ ] Level selected based on use case
  - [ ] Strong for critical data, Eventually for throughput

### pgvector Setup

- [ ] **Extension installation**
  - [ ] `CREATE EXTENSION vector` executed
  - [ ] PostgreSQL version compatible (14+)

- [ ] **Table design**
  - [ ] Vector column with correct dimensions
  - [ ] Appropriate data types for metadata
  - [ ] Primary key defined

- [ ] **Index creation**
  - [ ] HNSW index for production (not IVFFlat)
  - [ ] Operator class selected (vector_cosine_ops, etc.)
  - [ ] Index parameters tuned (m, ef_construction)

- [ ] **Connection pooling**
  - [ ] PgBouncer or similar configured
  - [ ] Pool size appropriate for load

### Pinecone Setup

- [ ] **Account configuration**
  - [ ] API key generated and secured
  - [ ] Environment/region selected

- [ ] **Index creation**
  - [ ] Dimension matches embedding model
  - [ ] Metric selected (cosine, euclidean, dotproduct)
  - [ ] Pod type or serverless selected
  - [ ] Replicas configured for availability

- [ ] **Namespace strategy**
  - [ ] Multi-tenancy via namespaces planned
  - [ ] Naming convention established

### Chroma Setup

- [ ] **Client mode**
  - [ ] In-memory for development
  - [ ] Persistent for testing

- [ ] **Collection configuration**
  - [ ] Distance function selected
  - [ ] Metadata schema planned

---

## Performance Tuning Checklist

### Index Optimization

- [ ] **HNSW tuning**
  - [ ] M parameter: Start with 16, increase for higher recall
  - [ ] ef_construction: 100-200 for good index quality
  - [ ] ef_search: Tune based on latency/recall tradeoff
  - [ ] Benchmark different configurations

- [ ] **Quantization (if needed)**
  - [ ] Evaluate scalar quantization first (4x memory reduction)
  - [ ] Test binary quantization for cost-sensitive workloads
  - [ ] Enable rescoring to recover accuracy
  - [ ] Measure recall impact before/after

### Query Optimization

- [ ] **Batch operations**
  - [ ] Batch size optimized (100-500 for upserts)
  - [ ] Async operations where possible
  - [ ] Connection pooling enabled

- [ ] **Search parameters**
  - [ ] score_threshold set to filter low-quality results
  - [ ] with_vectors=false unless needed
  - [ ] Limit set appropriately (not too high)

- [ ] **Filtering optimization**
  - [ ] Payload/metadata indexes created
  - [ ] Filters use indexed fields
  - [ ] Pre-filtering vs post-filtering evaluated

### Caching Strategy

- [ ] **Query caching**
  - [ ] Common queries identified
  - [ ] Cache layer implemented (Redis, in-memory)
  - [ ] TTL configured based on data freshness needs

- [ ] **Embedding caching**
  - [ ] Frequently queried embeddings cached
  - [ ] Cache key strategy defined
  - [ ] Cache invalidation on updates

### Resource Optimization

- [ ] **Memory management**
  - [ ] Quantization enabled if memory-constrained
  - [ ] On-disk storage for large payloads
  - [ ] Memory limits set appropriately

- [ ] **CPU optimization**
  - [ ] Connection pooling to reduce overhead
  - [ ] Batch operations to amortize costs
  - [ ] gRPC preferred over HTTP (Qdrant)

- [ ] **Storage optimization**
  - [ ] Tiered storage configured (hot/cold)
  - [ ] Compression enabled if supported
  - [ ] Regular compaction/vacuum

---

## Production Readiness Checklist

### High Availability

- [ ] **Replication**
  - [ ] Replicas configured for read scaling
  - [ ] Replication factor meets availability needs
  - [ ] Leader election configured (distributed systems)

- [ ] **Failover**
  - [ ] Automatic failover tested
  - [ ] Recovery time objective (RTO) validated
  - [ ] Health checks configured

- [ ] **Load balancing**
  - [ ] Load balancer in front of replicas
  - [ ] Health check endpoints configured
  - [ ] Sticky sessions if needed

### Backup & Recovery

- [ ] **Backup strategy**
  - [ ] Snapshot schedule configured
  - [ ] Backup storage location secured
  - [ ] Retention policy defined

- [ ] **Recovery testing**
  - [ ] Restore procedure documented
  - [ ] Recovery point objective (RPO) validated
  - [ ] Disaster recovery drill completed

- [ ] **Data export**
  - [ ] Export mechanism tested
  - [ ] Migration path to alternative DB documented

### Monitoring & Alerting

- [ ] **Metrics collection**
  - [ ] Query latency (p50, p95, p99)
  - [ ] Throughput (QPS)
  - [ ] Error rates
  - [ ] Index coverage
  - [ ] Storage utilization
  - [ ] Memory usage

- [ ] **Alerting rules**
  - [ ] High latency alerts
  - [ ] Error rate spike alerts
  - [ ] Storage threshold alerts
  - [ ] Memory pressure alerts
  - [ ] Replication lag alerts

- [ ] **Dashboards**
  - [ ] Operational dashboard created
  - [ ] Business metrics dashboard (if applicable)
  - [ ] On-call runbook documented

### Security

- [ ] **Authentication**
  - [ ] API keys rotated regularly
  - [ ] Service accounts with minimal permissions
  - [ ] No hardcoded credentials

- [ ] **Encryption**
  - [ ] TLS for data in transit
  - [ ] Encryption at rest enabled
  - [ ] Key management strategy defined

- [ ] **Access control**
  - [ ] Network segmentation (VPC, firewall)
  - [ ] IP allowlisting if applicable
  - [ ] Audit logging enabled

- [ ] **Data protection**
  - [ ] PII handling documented
  - [ ] Data retention policy implemented
  - [ ] Right to deletion process defined

### Operations

- [ ] **Deployment**
  - [ ] Blue-green or rolling deployment configured
  - [ ] Rollback procedure documented
  - [ ] Version pinning for reproducibility

- [ ] **Scaling**
  - [ ] Horizontal scaling tested
  - [ ] Auto-scaling configured if available
  - [ ] Capacity planning documented

- [ ] **Maintenance**
  - [ ] Index rebuild procedure documented
  - [ ] Compaction/vacuum schedule set
  - [ ] Upgrade procedure tested

---

## Migration Checklist

### Pre-Migration

- [ ] Source data inventory completed
- [ ] Target schema designed
- [ ] Mapping document created
- [ ] Test data exported and validated
- [ ] Migration scripts developed
- [ ] Rollback plan documented

### Migration Execution

- [ ] Maintenance window scheduled
- [ ] Source data exported
- [ ] Data transformed to target format
- [ ] Data loaded to target database
- [ ] Indexes created and built
- [ ] Data validation completed

### Post-Migration

- [ ] Application updated to use new database
- [ ] Performance benchmarks validated
- [ ] Monitoring confirmed working
- [ ] Source data archived
- [ ] Documentation updated
- [ ] Team trained on new system

---

## Troubleshooting Checklist

### Slow Queries

- [ ] Check if index exists and is being used
- [ ] Verify ef_search/nprobe parameters
- [ ] Check if filters are using indexed fields
- [ ] Review query complexity
- [ ] Check resource utilization (CPU, memory)
- [ ] Look for network latency issues

### Low Recall

- [ ] Verify embedding quality (model appropriate for data)
- [ ] Check distance metric matches embedding model
- [ ] Increase ef_search/nprobe
- [ ] Review quantization impact
- [ ] Validate data preprocessing consistency

### High Memory Usage

- [ ] Enable quantization
- [ ] Move payloads to disk
- [ ] Reduce HNSW M parameter
- [ ] Implement data partitioning
- [ ] Review batch sizes

### Ingestion Issues

- [ ] Check batch sizes (too large causes timeouts)
- [ ] Verify vector dimensions match schema
- [ ] Review payload size limits
- [ ] Check connection pool exhaustion
- [ ] Look for disk space issues

---

*Checklists v2.0*
*Part of vector-databases skill*
