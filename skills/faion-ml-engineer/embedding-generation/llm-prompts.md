# LLM Prompts for Embedding Tasks

## Model Selection Prompt

```
You are an ML engineer helping select the right embedding model.

Given the following requirements:
- Use case: {use_case}
- Document volume: {volume}
- Latency requirement: {latency}
- Budget: {budget}
- Privacy constraints: {privacy}
- Languages: {languages}

Recommend the best embedding model considering:

1. **Provider options:**
   - OpenAI text-embedding-3-large (3072d, $0.13/1M, MTEB 64.6)
   - OpenAI text-embedding-3-small (1536d, $0.02/1M, MTEB 62.3)
   - Cohere embed-v4 (1024d, $0.10/1M, MTEB 65.2, multilingual)
   - Voyage voyage-3-large (1536d, $0.12/1M, MTEB 63.8)
   - Voyage voyage-3.5-lite (1024d, $0.02/1M, MTEB 66.1)
   - BGE-M3 (1024d, free, self-hosted, MTEB 63.0)
   - nomic-embed-text (768d, free, local/Ollama)

2. **Evaluation criteria:**
   - Quality (MTEB score, domain fit)
   - Cost (per 1M tokens)
   - Latency (API vs local)
   - Context window (max tokens)
   - Dimension (storage/speed tradeoff)

Provide recommendation with reasoning.
```

## Chunking Strategy Prompt

```
You are helping design a document chunking strategy for embeddings.

Document characteristics:
- Type: {doc_type} (e.g., legal contracts, technical docs, articles)
- Average length: {avg_length}
- Structure: {structure} (e.g., headers, paragraphs, tables)
- Query patterns: {query_patterns}

Embedding model:
- Context window: {context_window} tokens
- Optimal chunk size: typically 256-512 tokens for retrieval

Design chunking strategy considering:

1. **Chunk size:** Balance context vs specificity
2. **Overlap:** Prevent information loss at boundaries
3. **Boundaries:** Respect semantic units (paragraphs, sections)
4. **Metadata:** What to preserve for filtering

Output format:
- Recommended chunk size (tokens)
- Overlap size (tokens)
- Boundary rules
- Metadata to extract
- Code example
```

## Cache Strategy Prompt

```
You are designing an embedding cache strategy for a production system.

System characteristics:
- Query volume: {qps} queries per second
- Unique query rate: {unique_rate}% new queries
- Document corpus size: {corpus_size}
- Latency SLA: {latency_sla}
- Budget: {budget}

Current metrics:
- Average embedding latency: {embedding_latency}ms
- Cache hit rate: {current_hit_rate}%

Design caching strategy considering:

1. **Cache layers:**
   - Exact match (hash-based)
   - Semantic cache (similarity threshold)
   - Hot/cold storage tiers

2. **Infrastructure:**
   - Redis (sub-ms, in-memory)
   - Vector DB (ms, persistent)
   - Disk cache (10s ms, cheap)

3. **Optimization:**
   - Target hit rate: 60-80%
   - TTL strategy for dynamic content
   - Cache warming for common queries

Provide:
- Architecture diagram (text)
- Configuration recommendations
- Expected metrics improvement
```

## Batch Processing Optimization Prompt

```
You are optimizing batch embedding generation for {volume} documents.

Current setup:
- Model: {model}
- Batch size: {batch_size}
- Processing time: {current_time}
- Cost: {current_cost}

Hardware:
- GPU: {gpu_type} ({vram}GB VRAM)
- CPU: {cpu_cores} cores
- Memory: {ram}GB RAM

Optimize for:
- [ ] Throughput (docs/sec)
- [ ] Cost reduction
- [ ] Latency
- [ ] Memory efficiency

Provide optimization recommendations:

1. **Batch size tuning** (based on VRAM)
2. **Length-based sorting** (reduce padding)
3. **Token-count batching** (variable length)
4. **Parallel processing** (multi-GPU/region)
5. **Mixed precision** (FP16)
6. **Quantization** (INT8)

Include code examples for key optimizations.
```

## Quality Evaluation Prompt

```
You are evaluating embedding quality for a {use_case} application.

Test setup:
- Query set: {num_queries} queries
- Document corpus: {num_docs} documents
- Ground truth: {ground_truth_source}

Models to compare:
{model_list}

Evaluation metrics:
1. **Recall@K:** Relevant docs in top K
2. **MRR:** Mean reciprocal rank
3. **NDCG:** Normalized discounted cumulative gain
4. **Latency:** p50, p95, p99
5. **Cost:** Per 1000 queries

Generate evaluation code and report template:

```python
# Evaluation framework
def evaluate_model(model_name, queries, corpus, ground_truth):
    # Your evaluation code here
    pass
```

Include:
- Statistical significance testing
- A/B testing framework
- Monitoring dashboard metrics
```

## Dimension Reduction Prompt

```
You are optimizing embedding dimensions for production.

Current setup:
- Model: {model}
- Current dimensions: {current_dims}
- Storage: {storage_size}
- Query latency: {latency}

Constraints:
- Maximum acceptable recall loss: {max_recall_loss}%
- Target storage reduction: {storage_target}%
- Latency requirement: {latency_req}ms

Options to evaluate:

1. **Native reduction** (text-embedding-3 only)
   - API parameter: dimensions=256/512/1024

2. **PCA** (post-processing)
   - Requires fitting on corpus
   - Adds preprocessing step

3. **Quantization** (INT8)
   - 4x memory reduction
   - Minimal quality loss

4. **Matryoshka embeddings**
   - Multiple granularities in one vector
   - Flexible truncation

Recommend approach with tradeoff analysis:
- Quality vs storage vs latency chart
- Implementation code
- Benchmark methodology
```

## Troubleshooting Prompt

```
You are debugging embedding quality issues.

Symptoms:
{symptoms}

System details:
- Model: {model}
- Preprocessing: {preprocessing}
- Index type: {index_type}
- Similarity metric: {metric}

Common issues checklist:

1. **Model mismatch**
   - Query model != index model
   - Solution: Verify model consistency

2. **Preprocessing inconsistency**
   - Different cleaning for index vs query
   - Solution: Standardize preprocessing

3. **Wrong similarity metric**
   - Euclidean with unnormalized vectors
   - Solution: Use cosine or normalize first

4. **Token truncation**
   - Long docs silently truncated
   - Solution: Chunking strategy

5. **Empty/zero vectors**
   - Empty text produces zero vector
   - Solution: Filter empty inputs

6. **Fine-tuning drift**
   - Model updated, embeddings stale
   - Solution: Reindex after model changes

Diagnostic steps:
1. Log preprocessing for sample query
2. Compare query/doc embedding dimensions
3. Check vector norms (should be ~1 if normalized)
4. Test with known similar pairs
5. Verify index configuration

Provide diagnostic code and resolution steps.
```

## Migration Planning Prompt

```
You are planning embedding model migration.

Current state:
- Model: {current_model}
- Index size: {index_size} vectors
- Query volume: {qps} QPS
- Downtime tolerance: {downtime}

Target:
- Model: {target_model}
- Reason: {migration_reason}

Migration strategy options:

1. **Blue-green deployment**
   - Build new index in parallel
   - Switch traffic atomically
   - Requires 2x storage temporarily

2. **Gradual rollout**
   - Dual-write to both indexes
   - Route % traffic to new index
   - Compare metrics before full switch

3. **Offline reindex**
   - Scheduled maintenance window
   - Faster but requires downtime

4. **Streaming migration**
   - Reindex on read (lazy)
   - No downtime, slower queries initially

Recommend strategy with:
- Step-by-step plan
- Rollback procedure
- Monitoring checklist
- Risk assessment
```

## Cost Optimization Prompt

```
You are optimizing embedding costs for {monthly_volume} tokens/month.

Current spending:
- Model: {model}
- Monthly cost: ${current_cost}
- Usage pattern: {usage_pattern}

Optimization strategies:

1. **Model downgrade**
   - text-embedding-3-large → text-embedding-3-small
   - Savings: ~85%
   - Quality tradeoff: Check Recall@K impact

2. **Dimension reduction**
   - 3072d → 512d
   - Savings: Storage + compute
   - Use native API parameter

3. **Caching**
   - Target 60-80% hit rate
   - Savings: Proportional to hit rate

4. **Batching**
   - Reduce API call overhead
   - Optimal: 100-1000 items/batch

5. **Two-stage retrieval**
   - Cheap embeddings for recall
   - Expensive reranker for precision

6. **Self-hosted fallback**
   - BGE-M3 for high volume
   - API for low-latency/quality

Calculate ROI for each strategy:
| Strategy | Savings | Implementation Cost | Payback |
|----------|---------|---------------------|---------|
| ... | ... | ... | ... |

Recommend prioritized implementation plan.
```
