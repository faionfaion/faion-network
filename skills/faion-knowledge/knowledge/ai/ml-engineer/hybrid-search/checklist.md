# Hybrid Search Checklists

Comprehensive checklists for implementing, tuning, and evaluating hybrid search systems.

## Implementation Checklist

### Phase 1: Planning

- [ ] **Define requirements**
  - [ ] Target latency SLO (e.g., p95 < 200ms)
  - [ ] Corpus size (current and projected)
  - [ ] Query types (keyword-heavy, semantic, mixed)
  - [ ] Throughput requirements (QPS)
  - [ ] Availability requirements (99.9%+?)

- [ ] **Choose vector database**
  - [ ] Evaluate Weaviate (native hybrid, GraphQL)
  - [ ] Evaluate Qdrant (native sparse-dense, gRPC)
  - [ ] Evaluate Pinecone (managed, serverless)
  - [ ] Evaluate Elasticsearch (existing infra?)
  - [ ] Consider pgvector (existing PostgreSQL?)
  - [ ] Document decision and rationale

- [ ] **Choose embedding model**
  - [ ] Evaluate OpenAI text-embedding-3-small (1536d, $0.02/1M tokens)
  - [ ] Evaluate OpenAI text-embedding-3-large (3072d, higher quality)
  - [ ] Evaluate Cohere embed-v3 (1024d, multilingual)
  - [ ] Evaluate BGE-M3 (self-hosted, multilingual)
  - [ ] Evaluate Voyage AI (domain-specific options)
  - [ ] Benchmark on representative queries

- [ ] **Choose fusion method**
  - [ ] Start with RRF (k=60) as baseline
  - [ ] Plan linear combination experiments
  - [ ] Consider query-adaptive fusion later

### Phase 2: Infrastructure Setup

- [ ] **Vector database setup**
  - [ ] Provision database (local, cloud, or hybrid)
  - [ ] Configure authentication and networking
  - [ ] Set up monitoring (metrics, logs, alerts)
  - [ ] Configure backup and recovery
  - [ ] Document connection details and credentials

- [ ] **Index schema design**
  - [ ] Define document schema with required fields
  - [ ] Configure dense vector index (HNSW params)
  - [ ] Configure sparse/BM25 index (tokenizer, analyzers)
  - [ ] Add metadata fields for filtering
  - [ ] Plan for schema migrations

- [ ] **Embedding pipeline**
  - [ ] Set up embedding API client with retries
  - [ ] Implement batching (optimal batch size for API)
  - [ ] Add caching for repeated embeddings
  - [ ] Handle rate limits gracefully
  - [ ] Monitor embedding costs

### Phase 3: Indexing Pipeline

- [ ] **Document preprocessing**
  - [ ] Implement text extraction (PDF, HTML, etc.)
  - [ ] Define chunking strategy (size, overlap)
  - [ ] Handle metadata extraction
  - [ ] Implement deduplication
  - [ ] Add content validation

- [ ] **Batch indexing**
  - [ ] Implement parallel embedding generation
  - [ ] Add progress tracking and logging
  - [ ] Handle failures with retry logic
  - [ ] Implement incremental indexing
  - [ ] Add index refresh/rebuild capability

- [ ] **Real-time indexing**
  - [ ] Set up document change detection
  - [ ] Implement async indexing queue
  - [ ] Handle document updates and deletes
  - [ ] Monitor indexing lag

### Phase 4: Query Pipeline

- [ ] **Query preprocessing**
  - [ ] Implement query cleaning/normalization
  - [ ] Add query expansion (optional)
  - [ ] Implement query classification (for adaptive alpha)
  - [ ] Handle special characters and operators

- [ ] **Hybrid retrieval**
  - [ ] Implement parallel BM25 and vector search
  - [ ] Add fusion logic (RRF or linear)
  - [ ] Implement result deduplication
  - [ ] Add metadata filtering support
  - [ ] Handle empty results gracefully

- [ ] **Reranking (optional)**
  - [ ] Choose reranker model
  - [ ] Implement reranking pipeline
  - [ ] Configure candidate pool size (typically 100)
  - [ ] Monitor reranker latency and costs

### Phase 5: API and Integration

- [ ] **Search API**
  - [ ] Design API contract (request/response schema)
  - [ ] Implement search endpoint
  - [ ] Add pagination support
  - [ ] Implement filtering and faceting
  - [ ] Add request validation

- [ ] **Error handling**
  - [ ] Handle database connection failures
  - [ ] Handle embedding API failures
  - [ ] Implement circuit breakers
  - [ ] Add graceful degradation (fallback to BM25)
  - [ ] Return meaningful error messages

- [ ] **Observability**
  - [ ] Add request logging (query, latency, results)
  - [ ] Implement distributed tracing
  - [ ] Set up latency dashboards
  - [ ] Create alerting rules
  - [ ] Track search quality metrics

---

## Tuning Checklist

### BM25 Tuning

- [ ] **Tokenization analysis**
  - [ ] Review tokenizer output on sample queries
  - [ ] Check language-specific handling
  - [ ] Evaluate stop word removal
  - [ ] Test stemming/lemmatization impact
  - [ ] Consider custom tokenizer if needed

- [ ] **Parameter tuning**
  - [ ] Experiment with k1 values (1.2, 1.5, 2.0)
  - [ ] Experiment with b values (0.5, 0.75, 0.9)
  - [ ] Measure impact on evaluation set
  - [ ] Document optimal parameters

- [ ] **Field boosting**
  - [ ] Identify high-value fields (title, summary)
  - [ ] Configure field weights
  - [ ] Test multi-field queries
  - [ ] Balance precision vs recall

### Vector Search Tuning

- [ ] **Embedding quality**
  - [ ] Evaluate embedding model on domain data
  - [ ] Test embedding dimensionality (384, 768, 1536)
  - [ ] Consider domain fine-tuning if needed
  - [ ] Benchmark retrieval quality

- [ ] **HNSW parameters**
  - [ ] Tune M (connections per node, typically 16-64)
  - [ ] Tune efConstruction (build quality, 100-200)
  - [ ] Tune ef (search quality, 50-200)
  - [ ] Balance recall vs latency

- [ ] **Quantization (if needed)**
  - [ ] Evaluate scalar quantization impact
  - [ ] Evaluate product quantization impact
  - [ ] Measure recall degradation
  - [ ] Document memory savings

### Fusion Tuning

- [ ] **RRF parameter**
  - [ ] Test k values (20, 40, 60, 100)
  - [ ] Measure impact on different query types
  - [ ] Document optimal k

- [ ] **Linear combination**
  - [ ] Test alpha values (0.3, 0.5, 0.7)
  - [ ] Implement score normalization
  - [ ] Compare min-max vs z-score normalization
  - [ ] Segment by query type if beneficial

- [ ] **Query-adaptive fusion**
  - [ ] Define query classification rules
  - [ ] Map query types to alpha values
  - [ ] Test on held-out query set
  - [ ] Implement and monitor in production

### Reranker Tuning

- [ ] **Candidate pool size**
  - [ ] Test with 50, 100, 200 candidates
  - [ ] Measure recall@k impact
  - [ ] Balance quality vs latency
  - [ ] Document optimal pool size

- [ ] **Model selection**
  - [ ] Benchmark multiple rerankers on domain data
  - [ ] Evaluate cross-encoder vs bi-encoder
  - [ ] Consider multilingual requirements
  - [ ] Document model choice and rationale

- [ ] **Latency optimization**
  - [ ] Implement batching for reranker
  - [ ] Consider GPU acceleration
  - [ ] Test early stopping techniques
  - [ ] Monitor p50/p95/p99 latencies

---

## Evaluation Checklist

### Dataset Preparation

- [ ] **Query set creation**
  - [ ] Collect 100+ representative queries
  - [ ] Include different query types (keyword, natural language)
  - [ ] Include edge cases (empty results, very long queries)
  - [ ] Document query source and selection criteria

- [ ] **Relevance labeling**
  - [ ] Define relevance scale (binary or graded)
  - [ ] Create annotation guidelines
  - [ ] Label queries with relevant documents
  - [ ] Calculate inter-annotator agreement
  - [ ] Use 3+ annotators for quality queries

- [ ] **Test set management**
  - [ ] Split into dev/test sets
  - [ ] Keep test set hidden during tuning
  - [ ] Version control labeled data
  - [ ] Plan for periodic refresh

### Offline Evaluation

- [ ] **Ranking metrics**
  - [ ] Calculate NDCG@k (k=5, 10, 20)
  - [ ] Calculate MRR (Mean Reciprocal Rank)
  - [ ] Calculate Precision@k
  - [ ] Calculate Recall@k
  - [ ] Compare against baselines

- [ ] **Component analysis**
  - [ ] Evaluate BM25 alone
  - [ ] Evaluate vector search alone
  - [ ] Evaluate hybrid without reranking
  - [ ] Evaluate hybrid with reranking
  - [ ] Document contribution of each component

- [ ] **Error analysis**
  - [ ] Identify systematic failure patterns
  - [ ] Analyze queries where hybrid underperforms
  - [ ] Check for embedding model blind spots
  - [ ] Document improvement opportunities

### Online Evaluation

- [ ] **A/B testing setup**
  - [ ] Define success metrics (CTR, conversion, satisfaction)
  - [ ] Calculate required sample size
  - [ ] Implement experiment infrastructure
  - [ ] Set up metric tracking

- [ ] **Experiments to run**
  - [ ] Test RRF vs linear fusion
  - [ ] Test different alpha values
  - [ ] Test with/without reranking
  - [ ] Test different reranker models

- [ ] **Analysis**
  - [ ] Monitor metric significance
  - [ ] Segment results by query type
  - [ ] Check for negative impacts on any segment
  - [ ] Document and socialize findings

### Continuous Monitoring

- [ ] **Quality metrics**
  - [ ] Track click-through rate on results
  - [ ] Monitor zero-result query rate
  - [ ] Track user feedback signals
  - [ ] Set up quality regression alerts

- [ ] **Performance metrics**
  - [ ] Monitor latency percentiles (p50, p95, p99)
  - [ ] Track throughput (QPS)
  - [ ] Monitor error rates
  - [ ] Track embedding API costs

- [ ] **Operational health**
  - [ ] Monitor index freshness
  - [ ] Track database resource usage
  - [ ] Set up capacity planning alerts
  - [ ] Document runbook for common issues

---

## Production Readiness Checklist

### Security

- [ ] API authentication implemented
- [ ] Rate limiting configured
- [ ] Input validation and sanitization
- [ ] PII handling documented
- [ ] Access controls for admin operations

### Reliability

- [ ] Database replication configured
- [ ] Automatic failover tested
- [ ] Backup and restore tested
- [ ] Disaster recovery plan documented
- [ ] Chaos testing performed

### Scalability

- [ ] Load testing performed
- [ ] Horizontal scaling tested
- [ ] Auto-scaling configured (if applicable)
- [ ] Capacity planning documented
- [ ] Cost projections created

### Operability

- [ ] Runbooks created for common issues
- [ ] On-call rotation established
- [ ] Incident response process defined
- [ ] Metrics dashboards created
- [ ] Alert thresholds tuned

### Documentation

- [ ] API documentation published
- [ ] Architecture diagram created
- [ ] Configuration reference documented
- [ ] Troubleshooting guide written
- [ ] Performance tuning guide created

---

## Quick Reference: Optimal Starting Points

| Component | Recommended Default | Tune When |
|-----------|---------------------|-----------|
| Fusion method | RRF (k=60) | Quality plateau |
| Alpha | 0.5 | Query types vary |
| Reranker candidates | 100 | Recall issues |
| HNSW M | 16 | Memory constrained |
| HNSW ef | 100 | Latency issues |
| BM25 k1 | 1.5 | Short docs dominate |
| BM25 b | 0.75 | Doc length varies |
| Embedding model | text-embedding-3-small | Quality issues |
| Chunk size | 512 tokens | Context issues |
| Chunk overlap | 50 tokens | Boundary issues |
