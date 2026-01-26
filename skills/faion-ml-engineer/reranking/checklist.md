# Reranking Checklists

Comprehensive checklists for model selection, implementation, and evaluation of reranking systems.

---

## Model Selection Checklist

### Requirements Gathering

- [ ] **Define accuracy requirements**
  - [ ] Target nDCG@k, MRR, or recall metric
  - [ ] Acceptable false positive/negative rates
  - [ ] Comparison baseline (no reranking)

- [ ] **Define latency requirements**
  - [ ] Maximum acceptable p50 latency
  - [ ] Maximum acceptable p99 latency
  - [ ] User-facing vs. background processing

- [ ] **Define scale requirements**
  - [ ] Expected queries per second (QPS)
  - [ ] Peak traffic multiplier
  - [ ] Documents per rerank call (candidate pool size)

- [ ] **Define infrastructure constraints**
  - [ ] GPU availability (type, count)
  - [ ] CPU-only deployment needed?
  - [ ] Cloud provider restrictions
  - [ ] Air-gapped environment?

- [ ] **Define data requirements**
  - [ ] Languages supported (single vs. multilingual)
  - [ ] Domain (general vs. specialized)
  - [ ] Document length (short passages vs. long docs)

- [ ] **Define cost constraints**
  - [ ] Budget for API calls (if applicable)
  - [ ] Infrastructure budget (GPU hours)
  - [ ] Total cost per 1M rerank operations

### Model Evaluation Matrix

| Criterion | Weight | Model A | Model B | Model C |
|-----------|--------|---------|---------|---------|
| Accuracy (nDCG@10) | 30% | | | |
| Latency (p50) | 25% | | | |
| Cost per 1M calls | 20% | | | |
| Language support | 10% | | | |
| Ease of integration | 10% | | | |
| License compatibility | 5% | | | |
| **Weighted Score** | 100% | | | |

### Model Shortlisting

#### For API-based deployment:
- [ ] Cohere Rerank 3 / Nimble evaluated
- [ ] Jina AI API evaluated
- [ ] Pinecone Rerank evaluated
- [ ] ZeroEntropy zerank-1 evaluated

#### For self-hosted deployment:
- [ ] BGE Reranker v2-M3 evaluated
- [ ] Jina Reranker v3 evaluated
- [ ] MS MARCO MiniLM variants evaluated
- [ ] FlashRank evaluated

#### For maximum accuracy:
- [ ] BGE Layerwise (Gemma/MiniCPM) evaluated
- [ ] Jina Reranker v3 evaluated

#### For minimum latency:
- [ ] MS MARCO MiniLM-L6 evaluated
- [ ] FlashRank evaluated
- [ ] Cohere Nimble evaluated

### Final Selection Validation

- [ ] Benchmark on representative sample of your data
- [ ] Verify latency meets requirements under load
- [ ] Confirm cost projections are acceptable
- [ ] Verify license terms allow your use case
- [ ] Test multilingual performance (if needed)
- [ ] Validate long document handling (if needed)

---

## Implementation Checklist

### Pre-Implementation

- [ ] **Architecture design**
  - [ ] Define two-stage vs. multi-stage pipeline
  - [ ] Determine candidate pool size (typically 50-100)
  - [ ] Define final top-k for LLM context
  - [ ] Plan fallback strategy if reranker fails

- [ ] **Infrastructure setup**
  - [ ] Provision GPU instances (if self-hosted)
  - [ ] Configure model serving (Triton, vLLM, etc.)
  - [ ] Set up API credentials (if using service)
  - [ ] Configure load balancing

- [ ] **Dependencies**
  - [ ] Install required packages
  - [ ] Pin package versions
  - [ ] Test in isolated environment
  - [ ] Document all dependencies

### Core Implementation

- [ ] **Reranker initialization**
  - [ ] Model loading with proper device placement
  - [ ] Warm-up inference to avoid cold start
  - [ ] Connection pooling for API clients
  - [ ] Timeout configuration

- [ ] **Input preprocessing**
  - [ ] Document truncation strategy defined
  - [ ] Query preprocessing (if needed)
  - [ ] Encoding/tokenization handled
  - [ ] Input validation implemented

- [ ] **Scoring implementation**
  - [ ] Batch processing for efficiency
  - [ ] Score normalization (if combining with other signals)
  - [ ] Tie-breaking strategy defined
  - [ ] Null/empty input handling

- [ ] **Output formatting**
  - [ ] Consistent output schema
  - [ ] Original metadata preserved
  - [ ] Scores included in output
  - [ ] Ranking order verified

### Error Handling

- [ ] **Graceful degradation**
  - [ ] Fallback to first-stage results if reranker fails
  - [ ] Partial failure handling (some docs fail)
  - [ ] Timeout handling with fallback
  - [ ] Rate limit handling (for APIs)

- [ ] **Retry logic**
  - [ ] Exponential backoff implemented
  - [ ] Maximum retry count defined
  - [ ] Circuit breaker pattern (optional)
  - [ ] Idempotency ensured

- [ ] **Logging and alerting**
  - [ ] Error logging with context
  - [ ] Latency logging per request
  - [ ] Alerting on error rate threshold
  - [ ] Alerting on latency threshold

### Performance Optimization

- [ ] **Batching**
  - [ ] Optimal batch size determined
  - [ ] Request batching for APIs
  - [ ] GPU batch inference optimized
  - [ ] Dynamic batching (if available)

- [ ] **Caching**
  - [ ] Query-result caching strategy
  - [ ] Cache key design (query + candidates hash)
  - [ ] Cache TTL defined
  - [ ] Cache invalidation strategy

- [ ] **Parallelization**
  - [ ] Async inference (if supported)
  - [ ] Thread pool for CPU-bound work
  - [ ] GPU stream management
  - [ ] Connection pooling

### Integration

- [ ] **First-stage retrieval**
  - [ ] Candidate pool size configurable
  - [ ] Score passthrough from retrieval
  - [ ] Metadata preservation
  - [ ] Filter propagation

- [ ] **LLM integration**
  - [ ] Reranked results formatted for context
  - [ ] Score-based context ordering
  - [ ] Diversity selection (if needed)
  - [ ] Context length management

- [ ] **API design**
  - [ ] Consistent endpoint naming
  - [ ] Request/response schema documented
  - [ ] Versioning strategy
  - [ ] Rate limiting configured

---

## Evaluation Checklist

### Test Data Preparation

- [ ] **Evaluation dataset**
  - [ ] Representative sample of production queries
  - [ ] Ground truth relevance labels
  - [ ] Multiple difficulty levels
  - [ ] Edge cases included

- [ ] **Query categories**
  - [ ] Simple factual queries
  - [ ] Multi-hop reasoning queries
  - [ ] Ambiguous queries
  - [ ] Negative/no-answer queries
  - [ ] Multilingual queries (if applicable)

- [ ] **Document variations**
  - [ ] Short passages
  - [ ] Long documents
  - [ ] Technical content
  - [ ] Conversational content

### Offline Evaluation Metrics

- [ ] **Ranking metrics**
  - [ ] nDCG@k (k = 1, 5, 10)
  - [ ] MRR (Mean Reciprocal Rank)
  - [ ] MAP (Mean Average Precision)
  - [ ] Precision@k / Recall@k

- [ ] **Comparison analysis**
  - [ ] Improvement over no-reranking baseline
  - [ ] Improvement over first-stage ranking
  - [ ] Statistical significance testing
  - [ ] Per-query-type breakdown

- [ ] **Error analysis**
  - [ ] False positives (irrelevant ranked high)
  - [ ] False negatives (relevant ranked low)
  - [ ] Pattern identification in failures
  - [ ] Edge case behavior

### Latency Evaluation

- [ ] **Latency profiling**
  - [ ] p50, p90, p99 latency measured
  - [ ] Cold start latency measured
  - [ ] Batch size impact analyzed
  - [ ] Candidate pool size impact analyzed

- [ ] **Resource usage**
  - [ ] CPU utilization under load
  - [ ] GPU utilization under load
  - [ ] Memory consumption
  - [ ] Network bandwidth (for APIs)

- [ ] **Scalability testing**
  - [ ] QPS limits identified
  - [ ] Horizontal scaling verified
  - [ ] Degradation pattern understood
  - [ ] Auto-scaling triggers configured

### Cost Evaluation

- [ ] **Direct costs**
  - [ ] API cost per 1M requests
  - [ ] Infrastructure cost per 1M requests
  - [ ] Total cost of ownership calculated

- [ ] **Cost optimization opportunities**
  - [ ] Caching effectiveness measured
  - [ ] Batching efficiency analyzed
  - [ ] Tier/plan optimization explored
  - [ ] Reserved capacity evaluated

### Online Evaluation

- [ ] **A/B testing setup**
  - [ ] Control group (no reranking)
  - [ ] Treatment group (with reranking)
  - [ ] Proper randomization
  - [ ] Sufficient sample size

- [ ] **Business metrics**
  - [ ] User satisfaction (if measurable)
  - [ ] RAG answer quality
  - [ ] Hallucination rate
  - [ ] User engagement metrics

- [ ] **Operational metrics**
  - [ ] Success rate
  - [ ] Timeout rate
  - [ ] Error rate
  - [ ] P95 latency in production

---

## Production Readiness Checklist

### Documentation

- [ ] Architecture diagram complete
- [ ] API documentation complete
- [ ] Runbook for common issues
- [ ] Troubleshooting guide

### Monitoring

- [ ] Latency dashboards configured
- [ ] Error rate dashboards configured
- [ ] Cost tracking dashboards configured
- [ ] Alerting rules defined

### Security

- [ ] API keys stored securely
- [ ] Input validation implemented
- [ ] Rate limiting configured
- [ ] Audit logging enabled

### Reliability

- [ ] Fallback mechanism tested
- [ ] Disaster recovery plan documented
- [ ] Backup model configured (if critical)
- [ ] Health check endpoint implemented

### Operations

- [ ] Deployment automation complete
- [ ] Rollback procedure documented
- [ ] On-call documentation ready
- [ ] Capacity planning documented

---

## Quick Decision Checklist

### Do I Need Reranking?

- [ ] First-stage retrieval quality < 80% of acceptable threshold
- [ ] High-stakes application (legal, medical, financial)
- [ ] Hybrid search fusion needed
- [ ] Can tolerate 100-500ms additional latency
- [ ] Quality improvement justifies complexity

**If 3+ checked:** Yes, implement reranking

### Which Model Should I Use?

Quick decision tree:

```
Need managed service?
├── Yes → Use Cohere Rerank 3 (or Nimble for speed)
└── No → Continue

Need multilingual?
├── Yes → Use Jina Reranker v3 or BGE v2-M3
└── No → Continue

Need maximum accuracy?
├── Yes → Use BGE Layerwise (Gemma)
└── No → Continue

Need minimum latency?
├── Yes → Use MS MARCO MiniLM-L6 or FlashRank
└── No → Use BGE Reranker v2-M3 (best balance)
```

### Is My Implementation Ready?

Must have:
- [ ] Error handling with fallback
- [ ] Latency monitoring
- [ ] Cost tracking (if API)
- [ ] Documented candidate pool size

Should have:
- [ ] Caching strategy
- [ ] Batch optimization
- [ ] A/B testing capability
- [ ] Evaluation metrics tracking
