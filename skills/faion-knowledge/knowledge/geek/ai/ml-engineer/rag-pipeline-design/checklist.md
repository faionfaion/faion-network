# RAG Pipeline Checklist

Production readiness verification for RAG systems.

---

## 1. Data Pipeline

### Ingestion
- [ ] Document loaders handle all required formats (PDF, MD, HTML, DOCX)
- [ ] Metadata extraction is configured (title, source, date, author)
- [ ] Incremental updates supported (not full re-index every time)
- [ ] Data versioning enabled for reproducibility
- [ ] Error handling for malformed documents

### Chunking
- [ ] Strategy selected based on document type
- [ ] Chunk size optimized (typically 400-800 tokens)
- [ ] Overlap configured (10-20% of chunk size)
- [ ] Sentence/paragraph boundaries respected
- [ ] Metadata preserved in chunks (source, position)
- [ ] Large tables/code blocks handled appropriately

### Embedding
- [ ] Model selected (quality vs cost tradeoff)
- [ ] Batch processing for efficiency
- [ ] Dimension matches vector DB configuration
- [ ] Same model used for queries and documents
- [ ] Rate limiting implemented for API-based models

### Storage
- [ ] Vector database selected and provisioned
- [ ] Index type configured (HNSW, IVF, etc.)
- [ ] Distance metric set (cosine, dot product, L2)
- [ ] Metadata indexing enabled for filtering
- [ ] Backup and recovery configured

---

## 2. Retrieval Layer

### Search Configuration
- [ ] Top-K tuned (typically 5-20)
- [ ] Similarity threshold set (filter low-quality results)
- [ ] Hybrid search enabled (vector + keyword)
- [ ] Metadata filters working
- [ ] Multi-query retrieval tested (if using)

### Query Processing
- [ ] Query preprocessing (cleaning, normalization)
- [ ] Query expansion/rewriting configured
- [ ] HyDE implemented (if beneficial for use case)
- [ ] Query embedding caching enabled

### Post-Retrieval
- [ ] Reranking model integrated (optional but recommended)
- [ ] Deduplication logic implemented
- [ ] Context compression working (if needed)
- [ ] Source diversity ensured

---

## 3. Generation Layer

### Prompt Engineering
- [ ] System prompt defines RAG behavior
- [ ] Context formatting is clear and consistent
- [ ] Source attribution instructions included
- [ ] "Don't know" instructions for missing context
- [ ] Output format specified

### LLM Configuration
- [ ] Model selected (quality vs cost vs latency)
- [ ] Temperature set appropriately (0.1-0.3 for factual)
- [ ] Max tokens configured
- [ ] Streaming enabled for long responses
- [ ] Fallback model configured

### Post-Processing
- [ ] Citation/source linking implemented
- [ ] Hallucination detection (if critical)
- [ ] Response validation against context
- [ ] Content filtering/guardrails active

---

## 4. Caching

### Embedding Cache
- [ ] Query embeddings cached (Redis, local)
- [ ] TTL configured based on query patterns
- [ ] Cache invalidation strategy defined

### Semantic Cache
- [ ] Similar query matching implemented
- [ ] Similarity threshold tuned
- [ ] Cache hit rate monitored

### Response Cache
- [ ] Identical queries cached
- [ ] Cache key includes all parameters
- [ ] TTL balanced (freshness vs performance)

### Knowledge Base Cache
- [ ] Frequently accessed chunks cached
- [ ] Hot/cold data separation
- [ ] Cache warming strategy

---

## 5. Orchestration

### Workflow
- [ ] Pipeline steps clearly defined
- [ ] Error handling at each step
- [ ] Timeouts configured
- [ ] Retry logic with backoff
- [ ] Circuit breakers for external services

### Scalability
- [ ] Horizontal scaling tested
- [ ] Load balancing configured
- [ ] Auto-scaling rules defined
- [ ] Resource limits set

### Async Processing
- [ ] Long-running tasks async
- [ ] Queue system in place (if needed)
- [ ] Batch processing optimized

---

## 6. Monitoring & Observability

### Metrics (Prometheus/Grafana)
- [ ] Query latency (p50, p95, p99)
- [ ] Retrieval latency
- [ ] Generation latency
- [ ] Token usage per query
- [ ] Cache hit rate
- [ ] Error rate
- [ ] Queries per second

### Quality Metrics
- [ ] Retrieval precision@K
- [ ] Retrieval recall@K
- [ ] Answer relevance score
- [ ] Groundedness score
- [ ] Context utilization

### Logging
- [ ] Queries logged (with privacy considerations)
- [ ] Retrieved chunks logged
- [ ] Generated responses logged
- [ ] Latency breakdown per component
- [ ] Error details captured

### Tracing
- [ ] End-to-end request tracing
- [ ] Component-level spans
- [ ] Trace ID propagation
- [ ] Tool: LangSmith / Langfuse / Jaeger

### Alerting
- [ ] Latency threshold alerts
- [ ] Error rate alerts
- [ ] Cost threshold alerts
- [ ] Quality degradation alerts

---

## 7. Security & Compliance

### Access Control
- [ ] API authentication implemented
- [ ] Rate limiting configured
- [ ] Document-level access control (if multi-tenant)
- [ ] Role-based permissions

### Data Privacy
- [ ] PII handling defined
- [ ] Data retention policy set
- [ ] Encryption at rest enabled
- [ ] Encryption in transit (TLS)
- [ ] Audit logging for sensitive access

### AI Safety
- [ ] Input validation/sanitization
- [ ] Prompt injection protection
- [ ] Output guardrails active
- [ ] Content moderation enabled

---

## 8. Cost Management

### Token Optimization
- [ ] Context length optimized
- [ ] Unnecessary retrieval minimized
- [ ] Query routing by complexity
- [ ] Cheaper models for simple queries

### Infrastructure
- [ ] Right-sized compute resources
- [ ] Spot/preemptible instances (where appropriate)
- [ ] Storage tiering configured
- [ ] Unused resources cleaned up

### Monitoring
- [ ] Cost per query tracked
- [ ] Monthly budget alerts
- [ ] Cost attribution by component
- [ ] Usage anomaly detection

---

## 9. Testing

### Unit Tests
- [ ] Chunking strategies tested
- [ ] Query processing tested
- [ ] Prompt formatting tested
- [ ] Error handling tested

### Integration Tests
- [ ] End-to-end pipeline tested
- [ ] Vector DB operations tested
- [ ] LLM API integration tested
- [ ] Cache operations tested

### Quality Tests
- [ ] Retrieval quality benchmark dataset
- [ ] Answer quality benchmark dataset
- [ ] Regression tests for known queries
- [ ] A/B testing framework ready

### Load Tests
- [ ] Concurrent users tested
- [ ] Sustained load tested
- [ ] Spike handling tested
- [ ] Resource limits verified

---

## 10. Documentation

### Technical
- [ ] Architecture diagram current
- [ ] Component dependencies documented
- [ ] API documentation complete
- [ ] Configuration guide available

### Operational
- [ ] Runbook for common issues
- [ ] Scaling procedures documented
- [ ] Incident response plan
- [ ] On-call rotation defined

### Knowledge Base
- [ ] Data sources documented
- [ ] Update procedures defined
- [ ] Quality criteria specified
- [ ] Schema/metadata documented

---

## Pre-Launch Verification

| Check | Status |
|-------|--------|
| All critical tests passing | [ ] |
| Monitoring dashboards operational | [ ] |
| Alerting rules active | [ ] |
| Rollback procedure tested | [ ] |
| Stakeholders informed | [ ] |
| Cost projections validated | [ ] |

---

## Post-Launch (First Week)

- [ ] Monitor query patterns
- [ ] Review error logs daily
- [ ] Check cost vs projections
- [ ] Gather initial user feedback
- [ ] Identify optimization opportunities
- [ ] Document lessons learned
