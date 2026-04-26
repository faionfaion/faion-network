# LLM Prompts for Hybrid Search

Structured prompts for implementing, optimizing, and debugging hybrid search systems with LLM assistance.

## Table of Contents

1. [Implementation Prompts](#implementation-prompts)
2. [Architecture Design Prompts](#architecture-design-prompts)
3. [Optimization Prompts](#optimization-prompts)
4. [Debugging Prompts](#debugging-prompts)
5. [Evaluation Prompts](#evaluation-prompts)
6. [Migration Prompts](#migration-prompts)

---

## Implementation Prompts

### Initial Setup Prompt

```markdown
# Hybrid Search Implementation Request

## Context
I need to implement a hybrid search system for a RAG application.

## Requirements
- **Corpus size**: [NUMBER] documents, [SIZE] total
- **Query volume**: [QPS] queries per second
- **Latency SLO**: p95 < [X]ms
- **Current infrastructure**: [LIST EXISTING SERVICES]
- **Budget constraints**: [MANAGED/SELF-HOSTED/MIXED]

## Technical Stack
- **Language**: [Python/TypeScript/Go]
- **Embedding model**: [MODEL NAME] ([DIMENSIONS]d)
- **Existing vector DB**: [DB NAME or "none"]
- **Existing keyword search**: [ES/OpenSearch/none]

## Request
Please provide:
1. Recommended architecture for my requirements
2. Vector database selection with rationale
3. Fusion method recommendation (RRF vs linear)
4. Complete implementation code for:
   - Index creation with proper schema
   - Document ingestion pipeline
   - Hybrid search function
   - Basic evaluation setup

## Constraints
- Must support metadata filtering on: [FIELDS]
- Must handle documents in: [LANGUAGES]
- [ANY OTHER CONSTRAINTS]
```

### Vector Database Integration Prompt

```markdown
# Vector Database Hybrid Search Integration

## Task
Implement hybrid search with [DATABASE NAME].

## Database Details
- **Database**: [Weaviate/Qdrant/Pinecone/Elasticsearch/pgvector]
- **Version**: [VERSION]
- **Deployment**: [Cloud/Self-hosted/Local]
- **Connection string**: [PROVIDED or "to be configured"]

## Existing Code
```python
# Paste any existing code here
```

## Requirements
1. Create collection/index with:
   - Dense vectors ([DIMENSIONS]d, [SIMILARITY] similarity)
   - Sparse vectors for BM25 (if supported)
   - Text field with proper analyzer
   - Metadata fields: [LIST FIELDS AND TYPES]

2. Implement functions:
   - `create_collection(name: str) -> None`
   - `upsert_documents(docs: list[Document]) -> int`
   - `hybrid_search(query: str, k: int, filters: dict) -> list[Result]`
   - `delete_document(doc_id: str) -> bool`

3. Include:
   - Error handling with retries
   - Connection pooling
   - Proper type hints
   - Docstrings

## Expected Output
Production-ready Python code with:
- All imports
- Configuration via environment variables
- Unit test stubs
```

### Fusion Implementation Prompt

```markdown
# Fusion Method Implementation

## Task
Implement [RRF/Linear/Query-Adaptive] fusion for hybrid search.

## Current State
I have separate results from:
- Vector search: `list[dict]` with `id`, `content`, `score` (cosine similarity)
- Keyword search: `list[dict]` with `id`, `content`, `score` (BM25)

## Requirements

### For RRF:
- Implement standard RRF with configurable k parameter
- Handle documents appearing in only one result set
- Preserve original scores for debugging

### For Linear:
- Implement min-max normalization
- Support configurable alpha (0=keyword, 1=vector)
- Add score attribution (show contribution from each source)

### For Query-Adaptive:
- Implement query classification rules
- Map query types to optimal alpha values
- Support:
  - Exact phrase detection (quotes)
  - Code/number detection
  - Question vs keyword queries
  - Short vs long queries

## Code Structure
```python
class FusionStrategy(ABC):
    @abstractmethod
    def fuse(self, vector_results: list, keyword_results: list, **kwargs) -> list:
        pass

# Implement concrete classes
```

## Include
- Type hints
- Docstrings with examples
- Unit tests for edge cases (empty results, single source, duplicates)
```

### Reranking Integration Prompt

```markdown
# Reranker Integration

## Task
Add reranking to my hybrid search pipeline using [Cohere/Jina/BGE/Custom].

## Current Pipeline
```python
# Paste current search function
```

## Requirements
1. Integrate [RERANKER] after fusion
2. Configure:
   - Model: [MODEL NAME]
   - Candidate pool size: [N] (default 100)
   - Final top_k: [K] (default 10)

3. Handle:
   - API rate limits with retries
   - Timeout handling
   - Fallback to non-reranked results on failure
   - Cost tracking

4. Add metrics:
   - Reranking latency
   - Score distribution before/after
   - API call count

## Provider Details
- **Provider**: [Cohere/Jina/Local]
- **API Key location**: [ENV_VAR or "to configure"]
- **Model**: [MODEL NAME]

## Expected Output
- Modified search function with reranking
- Separate reranker class for testing
- Configuration for enabling/disabling reranking
```

---

## Architecture Design Prompts

### System Design Prompt

```markdown
# Hybrid Search System Design

## Context
Design a production hybrid search system for:
- **Use case**: [DESCRIBE USE CASE]
- **Scale**: [DOCS] documents, [QPS] QPS, [USERS] concurrent users
- **Growth**: [EXPECTED GROWTH RATE]

## Current Infrastructure
- **Cloud**: [AWS/GCP/Azure/On-prem]
- **Orchestration**: [Kubernetes/ECS/Docker Compose/None]
- **Existing services**: [LIST]

## Requirements

### Functional
- Hybrid search with [RRF/linear] fusion
- Support for [N] document types
- Metadata filtering on [FIELDS]
- Multi-tenancy: [Yes/No]
- Real-time indexing: [Yes/No]

### Non-Functional
- Latency: p95 < [X]ms
- Availability: [99.9%/99.99%]
- Data retention: [PERIOD]
- Disaster recovery: [RPO/RTO]

### Budget
- Compute: [$X/month]
- Storage: [$X/month]
- API costs: [$X/month]

## Deliverables
1. Architecture diagram (described in text/mermaid)
2. Component selection with rationale:
   - Vector store
   - Keyword store
   - Caching layer
   - API gateway
3. Data flow for:
   - Indexing pipeline
   - Search request
   - Document update/delete
4. Scaling strategy
5. Monitoring and alerting plan
6. Cost estimation breakdown
```

### Database Selection Prompt

```markdown
# Vector Database Selection for Hybrid Search

## Decision Context
I need to select a vector database for hybrid search.

## Requirements Matrix

| Requirement | Priority | Notes |
|-------------|----------|-------|
| Native hybrid search | [High/Medium/Low] | [Notes] |
| Managed service option | [High/Medium/Low] | [Notes] |
| Self-hosted option | [High/Medium/Low] | [Notes] |
| Scale (vectors) | [High/Medium/Low] | [NUMBER] |
| Query latency | [High/Medium/Low] | < [X]ms |
| Filtering capability | [High/Medium/Low] | [COMPLEXITY] |
| Cost efficiency | [High/Medium/Low] | Budget: $[X]/month |
| Team expertise | [High/Medium/Low] | Know: [LIST] |

## Candidates to Evaluate
- Weaviate
- Qdrant
- Pinecone
- Milvus
- Elasticsearch
- pgvector
- [Others]

## Request
Provide:
1. Comparison matrix of candidates against requirements
2. Recommended choice with detailed rationale
3. Migration path if switching later
4. Hidden costs to consider
5. Red flags or limitations to watch for
```

### Embedding Model Selection Prompt

```markdown
# Embedding Model Selection

## Use Case
Hybrid search for [DOMAIN] documents.

## Requirements
- **Languages**: [LIST]
- **Document types**: [LIST]
- **Average document length**: [TOKENS]
- **Query types**: [Natural language/Keywords/Mixed]
- **Latency budget for embedding**: [X]ms
- **Cost sensitivity**: [High/Medium/Low]
- **Privacy requirements**: [Cloud OK/Must be local]

## Candidates
- OpenAI text-embedding-3-small (1536d)
- OpenAI text-embedding-3-large (3072d)
- Cohere embed-v3 (1024d)
- Voyage AI (domain-specific)
- BGE-M3 (local, multilingual)
- E5-mistral-7b-instruct (local, high quality)

## Request
1. Rank candidates for my use case
2. Provide benchmark expectations (if available)
3. Recommend embedding dimension (quality vs cost)
4. Suggest chunking strategy for chosen model
5. Estimate embedding costs at my scale
```

---

## Optimization Prompts

### Latency Optimization Prompt

```markdown
# Hybrid Search Latency Optimization

## Current State
- **p50 latency**: [X]ms
- **p95 latency**: [X]ms
- **p99 latency**: [X]ms
- **Target**: p95 < [Y]ms

## Latency Breakdown
| Component | Current (ms) | Target (ms) |
|-----------|--------------|-------------|
| Embedding | [X] | [Y] |
| Vector search | [X] | [Y] |
| Keyword search | [X] | [Y] |
| Fusion | [X] | [Y] |
| Reranking | [X] | [Y] |
| Network | [X] | [Y] |

## Current Implementation
```python
# Paste current search code
```

## Infrastructure
- **Vector DB**: [NAME], [SPECS]
- **Keyword DB**: [NAME], [SPECS]
- **Application**: [SPECS]
- **Network**: [TOPOLOGY]

## Constraints
- Cannot change: [LIST CONSTRAINTS]
- Budget for optimization: [$X]

## Request
1. Identify top 3 optimization opportunities
2. For each, provide:
   - Expected improvement
   - Implementation approach
   - Trade-offs
   - Effort estimate
3. Quick wins (< 1 day effort)
4. Long-term improvements (architecture changes)
```

### Memory Optimization Prompt

```markdown
# Vector Index Memory Optimization

## Current State
- **Vector count**: [N]
- **Dimensions**: [D]
- **Current memory**: [X] GB
- **Target memory**: [Y] GB
- **Acceptable recall loss**: [Z]%

## Current Configuration
```python
# Vector index configuration
```

## Request
1. Calculate theoretical memory requirements
2. Recommend quantization approach:
   - Scalar quantization
   - Product quantization
   - Binary quantization
3. HNSW parameter optimization for memory
4. Estimate recall impact for each option
5. Provide implementation code for chosen approach
```

### Cost Optimization Prompt

```markdown
# Hybrid Search Cost Optimization

## Current Costs (Monthly)
| Component | Cost | Notes |
|-----------|------|-------|
| Embedding API | $[X] | [PROVIDER] |
| Vector DB | $[X] | [PROVIDER] |
| Keyword DB | $[X] | [PROVIDER] |
| Reranker API | $[X] | [PROVIDER] |
| Compute | $[X] | [SPECS] |
| **Total** | $[X] | |

## Target Budget: $[Y]/month

## Usage Patterns
- Queries per month: [N]
- Documents indexed per month: [M]
- Average query complexity: [DETAILS]
- Peak hours: [TIMES]

## Request
1. Identify cost reduction opportunities
2. For each opportunity:
   - Estimated savings
   - Impact on quality/latency
   - Implementation complexity
3. Recommend caching strategy with expected hit rate
4. Evaluate self-hosted alternatives
5. Propose tiered architecture (hot/warm/cold)
```

### Alpha Tuning Prompt

```markdown
# Hybrid Search Alpha Tuning

## Context
I need to find the optimal alpha for linear fusion in my hybrid search.

## Current Setup
- **Alpha**: [CURRENT VALUE]
- **Evaluation set**: [N] queries with relevance judgments
- **Metrics tracked**: [NDCG@10, MRR, Recall@100]

## Current Performance
| Alpha | NDCG@10 | MRR | Recall@100 |
|-------|---------|-----|------------|
| 0.0 | [X] | [X] | [X] |
| 0.3 | [X] | [X] | [X] |
| 0.5 | [X] | [X] | [X] |
| 0.7 | [X] | [X] | [X] |
| 1.0 | [X] | [X] | [X] |

## Query Analysis
- **Keyword-heavy queries**: [N]% of total
- **Semantic queries**: [N]% of total
- **Mixed queries**: [N]% of total

## Request
1. Analyze the performance data
2. Recommend optimal fixed alpha
3. Design query-adaptive alpha rules
4. Suggest A/B test plan for validation
5. Provide code for query classification
```

---

## Debugging Prompts

### Poor Retrieval Quality Prompt

```markdown
# Hybrid Search Quality Debugging

## Problem
Hybrid search is returning irrelevant results for certain query types.

## Symptoms
- **Query type affected**: [DESCRIBE]
- **Expected results**: [DESCRIBE]
- **Actual results**: [DESCRIBE]
- **Frequency**: [X]% of queries

## Example Failing Queries
1. Query: "[QUERY 1]"
   - Expected: [DOC IDS]
   - Got: [DOC IDS]

2. Query: "[QUERY 2]"
   - Expected: [DOC IDS]
   - Got: [DOC IDS]

## Current Configuration
- **Fusion method**: [RRF/Linear]
- **Alpha**: [VALUE] (if linear)
- **RRF k**: [VALUE] (if RRF)
- **Embedding model**: [MODEL]
- **BM25 params**: k1=[X], b=[Y]

## Debug Data
```python
# For failing query, show:
# - BM25 results with scores
# - Vector results with scores
# - Fused results with scores
```

## Request
1. Diagnose the likely cause
2. Suggest specific fixes to try
3. Provide debugging code to isolate the issue
4. Recommend evaluation approach to validate fix
```

### Latency Spike Debugging Prompt

```markdown
# Latency Spike Investigation

## Problem
Experiencing intermittent latency spikes in hybrid search.

## Observations
- **Normal latency**: [X]ms p95
- **Spike latency**: [Y]ms p95
- **Spike frequency**: [PATTERN]
- **Spike duration**: [DURATION]
- **Correlation with**: [EVENTS if known]

## Metrics During Spikes
| Metric | Normal | During Spike |
|--------|--------|--------------|
| CPU | [X]% | [Y]% |
| Memory | [X]% | [Y]% |
| Network I/O | [X] | [Y] |
| Disk I/O | [X] | [Y] |
| DB connections | [X] | [Y] |
| Queue depth | [X] | [Y] |

## Infrastructure
- **Application**: [SPECS, REPLICAS]
- **Vector DB**: [SPECS, CONFIG]
- **Keyword DB**: [SPECS, CONFIG]
- **Load balancing**: [CONFIG]

## Logs/Traces
```
# Relevant log entries during spike
```

## Request
1. List likely causes in order of probability
2. For each cause:
   - How to confirm
   - How to fix
   - Prevention strategy
3. Provide monitoring queries to catch future spikes
4. Recommend alerting thresholds
```

### Index Corruption/Inconsistency Prompt

```markdown
# Index Inconsistency Debugging

## Problem
Vector and keyword indices are out of sync.

## Symptoms
- Documents found in vector search but not keyword search (or vice versa)
- Document counts differ between stores
- Updates not reflected consistently

## Counts
| Store | Expected | Actual | Difference |
|-------|----------|--------|------------|
| Vector | [X] | [Y] | [Z] |
| Keyword | [X] | [Y] | [Z] |

## Recent Changes
- [LIST RECENT CHANGES TO INDEXING PIPELINE]

## Indexing Code
```python
# Current indexing implementation
```

## Request
1. Identify likely causes of inconsistency
2. Provide reconciliation script to:
   - Identify missing documents in each store
   - Identify orphaned documents
   - Generate report of inconsistencies
3. Recommend fixes to prevent future inconsistencies
4. Suggest transactional indexing pattern
```

### Embedding Quality Debugging Prompt

```markdown
# Embedding Quality Investigation

## Problem
Semantic search component of hybrid search is underperforming.

## Evidence
- Similar documents have low cosine similarity
- Unrelated documents sometimes rank higher than relevant ones
- Performance degrades for [SPECIFIC DOMAIN/LANGUAGE]

## Examples
```python
# Example 1: Should be similar but isn't
doc1 = "[TEXT]"
doc2 = "[TEXT]"
similarity = [VALUE]  # Expected > 0.8

# Example 2: Shouldn't be similar but is
doc1 = "[TEXT]"
doc2 = "[TEXT]"
similarity = [VALUE]  # Expected < 0.3
```

## Current Setup
- **Embedding model**: [MODEL]
- **Chunking**: [SIZE] tokens, [OVERLAP] overlap
- **Preprocessing**: [STEPS]

## Request
1. Diagnose potential issues:
   - Model choice
   - Chunking strategy
   - Preprocessing problems
2. Provide analysis code to:
   - Visualize embedding clusters
   - Calculate intra/inter-class similarity
   - Identify outlier documents
3. Recommend improvements with expected impact
```

---

## Evaluation Prompts

### Evaluation Dataset Creation Prompt

```markdown
# Evaluation Dataset Creation

## Task
Create an evaluation dataset for hybrid search.

## Corpus Details
- **Domain**: [DOMAIN]
- **Document count**: [N]
- **Document types**: [TYPES]
- **Languages**: [LANGUAGES]

## Requirements
- **Query count**: [N] queries minimum
- **Relevance scale**: [Binary/Graded 0-3]
- **Query types to cover**:
  - Keyword queries (exact terms)
  - Semantic queries (conceptual)
  - Mixed queries
  - Edge cases (rare terms, typos, etc.)

## Request
1. Query generation strategy:
   - Methods to generate diverse queries
   - Coverage of different intents
   - Balance of difficulty levels

2. Relevance labeling approach:
   - Guidelines for annotators
   - Inter-annotator agreement protocol
   - Handling ambiguous cases

3. Provide code/prompts for:
   - Query generation using LLM
   - Semi-automated relevance labeling
   - Quality checks for the dataset

4. Recommend dataset size for statistical significance
```

### Evaluation Metrics Prompt

```markdown
# Hybrid Search Evaluation Metrics

## Context
I need to comprehensively evaluate my hybrid search system.

## Current Metrics
- [LIST CURRENT METRICS]

## Questions to Answer
1. Overall retrieval quality
2. Ranking effectiveness
3. Coverage vs precision trade-off
4. Component contribution (vector vs keyword)
5. Latency vs quality trade-off

## Request
Provide:
1. Complete metrics framework:
   - Metric name
   - Formula
   - Interpretation
   - When to use

2. Implementation code for:
   - NDCG@k
   - MRR
   - Precision@k
   - Recall@k
   - MAP
   - Hit rate

3. Statistical significance testing:
   - Paired t-test for metric comparison
   - Bootstrap confidence intervals
   - Sample size recommendations

4. Visualization recommendations:
   - Precision-recall curves
   - Rank distribution histograms
   - Component contribution charts
```

### A/B Testing Prompt

```markdown
# Hybrid Search A/B Test Design

## Experiment Goal
Test [CHANGE] in hybrid search.

## Hypothesis
[CHANGE] will improve [METRIC] by [X]% without degrading [OTHER METRIC] by more than [Y]%.

## Variants
- **Control**: Current implementation
- **Treatment**: [DESCRIBE CHANGE]

## Traffic and Duration
- **Available traffic**: [QPS]
- **Minimum detectable effect**: [X]%
- **Statistical power**: [80%/90%]
- **Significance level**: [0.05/0.01]

## Metrics
- **Primary**: [METRIC]
- **Secondary**: [METRICS]
- **Guardrails**: [METRICS THAT MUST NOT DEGRADE]

## Request
1. Calculate required sample size
2. Recommended test duration
3. Stratification strategy (by query type, user segment, etc.)
4. Implementation approach:
   - Traffic splitting
   - Metric collection
   - Result analysis
5. Decision framework:
   - When to ship
   - When to iterate
   - When to abandon
```

---

## Migration Prompts

### Vector Database Migration Prompt

```markdown
# Vector Database Migration

## Migration Details
- **From**: [CURRENT DB]
- **To**: [TARGET DB]
- **Vector count**: [N]
- **Downtime tolerance**: [ZERO/MINIMAL/SCHEDULED]

## Current Schema
```python
# Current index/collection schema
```

## Reasons for Migration
- [REASON 1]
- [REASON 2]

## Request
1. Migration strategy:
   - Dual-write approach
   - Bulk migration approach
   - Hybrid approach

2. Schema mapping:
   - Field mappings
   - Index configuration differences
   - Feature gaps to handle

3. Migration code:
   - Export from source
   - Transform if needed
   - Import to target
   - Verification

4. Rollback plan

5. Testing strategy:
   - Parallel query comparison
   - Performance benchmarking
   - Consistency validation

6. Cutover procedure:
   - Traffic switching
   - Monitoring during cutover
   - Success criteria
```

### Fusion Method Migration Prompt

```markdown
# Fusion Method Migration

## Current State
- **Fusion method**: [RRF/Linear]
- **Current performance**: [METRICS]

## Target State
- **New fusion method**: [METHOD]
- **Expected improvement**: [METRICS]

## Concerns
- [LIST CONCERNS ABOUT MIGRATION]

## Request
1. Gradual migration strategy
2. A/B test design for validation
3. Fallback mechanism
4. Code changes required
5. Monitoring additions needed
6. Rollback procedure
```

---

## Prompt Engineering Tips

### For Better Results

1. **Be specific about constraints**
   - Hardware limitations
   - Budget constraints
   - Latency requirements
   - Team expertise

2. **Provide context**
   - Existing code snippets
   - Current metrics
   - Error messages
   - Log samples

3. **Ask for trade-offs**
   - Every optimization has costs
   - Request explicit trade-off analysis

4. **Request validation**
   - Ask for tests with the code
   - Request metrics to verify success

5. **Iterate**
   - Start with high-level design
   - Drill down into specific components
   - Refine based on implementation feedback

### Prompt Structure

```markdown
# [Clear Title]

## Context
[Background information the LLM needs]

## Current State
[What exists today - code, metrics, infrastructure]

## Requirements
[What you need - functional, non-functional]

## Constraints
[Limitations - budget, time, expertise, infrastructure]

## Request
[Specific asks - numbered for clarity]

## Expected Output
[Format and completeness expectations]
```

---

## References

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Self-Consistency in LLMs](https://arxiv.org/abs/2203.11171)
