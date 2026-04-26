# LLM Prompts for Text Embeddings

Prompts for model selection, optimization, debugging, and implementation assistance.

---

## Table of Contents

1. [Model Selection Prompts](#model-selection-prompts)
2. [Optimization Prompts](#optimization-prompts)
3. [Debugging Prompts](#debugging-prompts)
4. [Implementation Prompts](#implementation-prompts)
5. [Evaluation Prompts](#evaluation-prompts)
6. [Cost Analysis Prompts](#cost-analysis-prompts)

---

## Model Selection Prompts

### General Model Selection

```
I need to select an embedding model for my project. Help me choose the best option.

**Use Case:**
[Describe your use case: semantic search, RAG, classification, clustering, etc.]

**Requirements:**
- Expected query volume: [queries/day]
- Document corpus size: [number of documents]
- Average document length: [tokens]
- Languages needed: [list languages]
- Maximum acceptable latency: [ms]
- Monthly budget: [$]
- Privacy constraints: [cloud API allowed / on-prem only]

**Current Setup:**
- Vector database: [Qdrant/Pinecone/pgvector/etc.]
- Tech stack: [Python/Node.js/etc.]

Please recommend:
1. Primary model choice with rationale
2. Alternative option for comparison
3. Dimension recommendation
4. Expected cost estimate
5. Implementation considerations
```

### RAG-Specific Model Selection

```
I'm building a RAG system and need to select the best embedding model.

**RAG Details:**
- Knowledge base type: [documentation, Q&A, support tickets, legal docs, etc.]
- Total documents: [number]
- Average document length: [pages/tokens]
- Query patterns: [short questions, long queries, keyword-heavy, conversational]
- Expected QPS: [queries per second]

**Quality Requirements:**
- Target Recall@10: [%]
- Acceptable false positive rate: [%]
- Need for exact keyword matching: [Yes/No]

**Constraints:**
- Latency budget: [ms for embedding + retrieval]
- Cost budget: [$/month]
- Can fine-tune: [Yes/No]

Please recommend:
1. Best embedding model for my use case
2. Whether to use hybrid search (embeddings + BM25)
3. Optimal chunk size and overlap
4. Reranking strategy if needed
5. Estimated infrastructure requirements
```

### Multilingual Model Selection

```
I need embeddings for a multilingual application.

**Languages:**
Primary: [list main languages]
Secondary: [list additional languages]
Mixed content: [Yes/No - documents contain multiple languages]

**Use Case:**
[cross-lingual search, monolingual search per language, translation matching, etc.]

**Volume:**
- Documents per language: [breakdown]
- Query distribution: [% per language]

**Quality Requirements:**
- Need same embedding space across languages: [Yes/No]
- Acceptable quality drop for low-resource languages: [%]

Please recommend:
1. Best multilingual model
2. Whether to use separate models per language
3. How to handle mixed-language documents
4. Testing strategy for multilingual quality
```

### Local vs Cloud Decision

```
Help me decide between local and cloud embedding models.

**Current Situation:**
- Monthly embedding volume: [tokens/month]
- Peak QPS: [queries/second]
- Available GPU: [type and count, or "none"]
- Available CPU cores: [count]
- Available RAM: [GB]

**Constraints:**
- Data sensitivity: [public / confidential / PII present]
- Compliance requirements: [GDPR, HIPAA, SOC2, etc.]
- Network reliability: [always connected / intermittent / air-gapped]
- Team ML expertise: [none / basic / advanced]

**Budget:**
- Cloud API budget: [$/month]
- Infrastructure budget: [$/month]
- One-time GPU investment: [$]

Please analyze:
1. Cost comparison (cloud vs local)
2. Quality comparison
3. Operational complexity
4. Recommended approach
5. Migration path if starting with one and switching later
```

---

## Optimization Prompts

### Cost Optimization

```
Help me optimize embedding costs for my production system.

**Current State:**
- Model: [model name]
- Monthly volume: [tokens embedded]
- Current monthly cost: [$]
- Cache hit rate: [%]
- Average batch size: [texts per request]

**Usage Patterns:**
- New documents per day: [count]
- Queries per day: [count]
- Duplicate/similar text ratio: [%]
- Document update frequency: [daily/weekly/rarely]

**Quality Baseline:**
- Current Recall@10: [%]
- Minimum acceptable Recall@10: [%]

Please suggest:
1. Quick wins (no quality impact)
2. Trade-offs (some quality for significant savings)
3. Architectural changes for long-term optimization
4. Expected savings for each recommendation
```

### Latency Optimization

```
Help me reduce embedding latency in my application.

**Current Performance:**
- Embedding latency (p50): [ms]
- Embedding latency (p95): [ms]
- Embedding latency (p99): [ms]
- Target latency (p95): [ms]

**Setup:**
- Model: [model name]
- Deployment: [API / local GPU / local CPU]
- Batch size: [current batch size]
- Concurrent requests: [count]

**Bottlenecks Identified:**
[List any known bottlenecks]

Please recommend:
1. Model-level optimizations
2. Infrastructure optimizations
3. Architectural patterns (caching, pre-computation)
4. Trade-offs to consider
5. Expected latency improvement for each change
```

### Quality Optimization

```
Help me improve embedding quality for my retrieval system.

**Current Metrics:**
- Recall@10: [%]
- MRR: [value]
- Precision@10: [%]

**Target Metrics:**
- Recall@10: [%]
- MRR: [value]

**System Details:**
- Model: [model name]
- Chunk size: [tokens]
- Chunk overlap: [tokens]
- Corpus size: [documents]

**Failure Analysis:**
[Describe common failure cases - what queries fail, what documents are missed]

Please suggest:
1. Model changes to consider
2. Chunking strategy improvements
3. Query preprocessing techniques
4. Hybrid search configuration
5. Fine-tuning approach if applicable
6. Evaluation methodology improvements
```

### Hybrid Search Configuration

```
Help me configure hybrid search (dense embeddings + sparse/BM25).

**Current Setup:**
- Dense model: [model name]
- Dense retrieval Recall@10: [%]
- Sparse/BM25 Recall@10: [%]
- Combined Recall@10: [%]

**Query Characteristics:**
- Average query length: [tokens]
- Keyword-heavy queries: [% of queries]
- Natural language queries: [% of queries]
- Exact match requirements: [description]

**Document Characteristics:**
- Technical jargon frequency: [low/medium/high]
- Acronyms and abbreviations: [common/rare]
- Entity names importance: [low/medium/high]

Please recommend:
1. Optimal alpha (dense weight) for my use case
2. Whether to use learned sparse (SPLADE) vs BM25
3. Normalization strategy for combining scores
4. Query routing rules (when to use dense vs sparse vs hybrid)
5. Evaluation strategy for tuning
```

---

## Debugging Prompts

### Poor Retrieval Quality

```
My embedding-based retrieval is performing poorly. Help me debug.

**Symptoms:**
- Expected Recall@10: [%]
- Actual Recall@10: [%]
- Specific failure patterns: [describe]

**Example Failures:**
Query: "[example query that fails]"
Expected documents: "[titles/snippets of expected results]"
Actual top results: "[titles/snippets of actual results]"

**System Configuration:**
- Embedding model: [model name]
- Dimensions: [number]
- Chunk size: [tokens]
- Vector DB: [name]
- Distance metric: [cosine/euclidean/dot product]

**Data Characteristics:**
- Document types: [description]
- Average document length: [tokens]
- Vocabulary characteristics: [technical, general, domain-specific]

Please help me:
1. Identify likely root causes
2. Diagnostic queries to run
3. Quick fixes to try
4. Systematic debugging approach
5. Metrics to track during debugging
```

### Dimension Mismatch Issues

```
I'm getting dimension mismatch errors in my embedding system.

**Error Message:**
[paste exact error]

**Setup:**
- Embedding model(s) used: [list]
- Expected dimensions: [number]
- Actual dimensions: [number]
- Vector database: [name]
- Index configuration: [details]

**History:**
- When did this start: [date/event]
- Recent changes: [model updates, config changes, etc.]

Please help me:
1. Diagnose the root cause
2. Fix the immediate issue
3. Prevent future occurrences
4. Handle existing data with wrong dimensions
```

### Slow Embedding Generation

```
Embedding generation is slower than expected. Help me diagnose.

**Performance:**
- Expected: [embeddings/second]
- Actual: [embeddings/second]
- Batch size: [number]

**Setup:**
- Model: [name]
- Hardware: [CPU/GPU specs]
- Memory: [available RAM/VRAM]
- Framework: [sentence-transformers, OpenAI SDK, etc.]

**Observations:**
- CPU utilization: [%]
- GPU utilization: [%]
- Memory usage: [%]
- Network latency (if API): [ms]

Please help me:
1. Identify the bottleneck
2. Optimize for my hardware
3. Benchmark properly
4. Set realistic expectations
```

### Inconsistent Results

```
I'm getting inconsistent embedding results for the same text.

**Symptoms:**
- Same text produces different embeddings: [always/sometimes]
- Magnitude of difference: [cosine similarity between runs]
- Affects: [single texts / batches / specific texts only]

**Setup:**
- Model: [name]
- Framework version: [version]
- Hardware: [description]
- Normalization: [yes/no]

**Code Sample:**
```python
[paste relevant code]
```

Please help me:
1. Identify causes of non-determinism
2. Make results reproducible
3. Quantify acceptable variance
4. Handle variance in production
```

---

## Implementation Prompts

### New Embedding Pipeline

```
Help me design an embedding pipeline for my project.

**Project Overview:**
[Brief description of the project]

**Requirements:**
- Data sources: [list sources]
- Update frequency: [real-time / batch / hybrid]
- Scale: [documents count, query volume]
- Latency requirements: [ms]
- Budget: [$/month]

**Tech Stack:**
- Language: [Python/Node.js/etc.]
- Database: [PostgreSQL/MongoDB/etc.]
- Vector DB: [chosen or need recommendation]
- Infrastructure: [cloud provider, kubernetes, etc.]

**Team:**
- ML experience: [none/basic/advanced]
- DevOps experience: [none/basic/advanced]

Please provide:
1. Architecture diagram (text description)
2. Component selection with rationale
3. Implementation phases
4. Code structure recommendation
5. Monitoring and alerting strategy
6. Estimated complexity for each phase
```

### Chunking Strategy Design

```
Help me design a chunking strategy for my documents.

**Document Types:**
[Describe document types: PDFs, HTML, markdown, etc.]

**Document Characteristics:**
- Average length: [pages/tokens]
- Structure: [headings, sections, paragraphs, lists]
- Code blocks: [yes/no, frequency]
- Tables: [yes/no, frequency]
- Images with captions: [yes/no]

**Query Patterns:**
- Query types: [factual, procedural, conceptual]
- Expected answer length: [sentence / paragraph / section]
- Need for context: [low / medium / high]

**Embedding Model:**
- Model: [name]
- Max tokens: [number]
- Optimal token range: [min-max]

Please recommend:
1. Chunking strategy (fixed, semantic, recursive)
2. Optimal chunk size with rationale
3. Overlap configuration
4. How to handle special elements (code, tables)
5. Metadata to preserve per chunk
6. Edge cases to handle
```

### Migration Between Models

```
Help me plan a migration from one embedding model to another.

**Current State:**
- Model: [current model]
- Dimensions: [number]
- Indexed documents: [count]
- Vector DB: [name]

**Target State:**
- Model: [new model]
- Dimensions: [number]
- Reason for migration: [quality, cost, features]

**Constraints:**
- Downtime tolerance: [none / minutes / hours]
- Recompute budget: [can recompute all / only new / incremental]
- Timeline: [deadline]

Please provide:
1. Migration strategy options
2. Recommended approach for my constraints
3. Step-by-step migration plan
4. Rollback plan
5. Validation strategy
6. Risk mitigation
```

---

## Evaluation Prompts

### Create Evaluation Dataset

```
Help me create an evaluation dataset for my embedding system.

**System Purpose:**
[Describe what the system does]

**Available Resources:**
- Existing queries: [yes/no, count]
- Query logs: [yes/no]
- User feedback: [yes/no]
- Domain experts: [yes/no]

**Corpus Characteristics:**
- Document count: [number]
- Document types: [description]
- Topics covered: [list main topics]

**Evaluation Goals:**
- Primary metric: [Recall@K / MRR / nDCG]
- Secondary metrics: [list]
- Specific scenarios to test: [list edge cases]

Please help me:
1. Design the evaluation dataset structure
2. Determine optimal dataset size
3. Create query generation strategy
4. Define relevance labeling guidelines
5. Handle edge cases and hard negatives
6. Establish baseline expectations
```

### Benchmark Comparison

```
Help me benchmark multiple embedding models for my use case.

**Models to Compare:**
1. [Model 1]
2. [Model 2]
3. [Model 3]

**Evaluation Criteria:**
- Quality: [metrics to measure]
- Speed: [latency, throughput]
- Cost: [per token, monthly estimate]
- Other: [specific requirements]

**Test Conditions:**
- Test dataset size: [count]
- Hardware: [specs]
- Batch sizes to test: [list]

Please provide:
1. Comprehensive evaluation plan
2. Metrics to capture
3. Statistical significance requirements
4. Visualization recommendations
5. Decision framework for final selection
```

### A/B Test Design

```
Help me design an A/B test for embedding models in production.

**Current Model:** [model A]
**Candidate Model:** [model B]

**Production Context:**
- Daily query volume: [count]
- User types: [description]
- Success metrics: [CTR, satisfaction, task completion]

**Constraints:**
- Risk tolerance: [low/medium/high]
- Test duration: [days/weeks]
- Traffic allocation: [% to new model]

Please help me:
1. Design the A/B test structure
2. Calculate required sample size
3. Define success criteria
4. Handle edge cases (new users, power users)
5. Plan for early stopping rules
6. Analyze and interpret results
```

---

## Cost Analysis Prompts

### Total Cost of Ownership

```
Help me calculate the total cost of ownership for my embedding infrastructure.

**Option A: Cloud API**
- Provider: [OpenAI/Voyage/Cohere]
- Model: [name]
- Monthly volume: [tokens]

**Option B: Self-hosted**
- Model: [name]
- Hardware needed: [GPU type, count]
- Cloud vs on-prem: [preference]

**Hidden Costs to Consider:**
- Engineering time: [hourly rate]
- Maintenance overhead: [hours/month]
- Monitoring/observability: [current tools]

**Timeline:**
- Project duration: [months/years]
- Expected growth rate: [% per month]

Please analyze:
1. Year 1 TCO comparison
2. Year 3 TCO comparison
3. Break-even point for self-hosting
4. Risk factors for each option
5. Recommendation with rationale
```

### Cost Projection

```
Help me project embedding costs as my system scales.

**Current State:**
- Monthly volume: [tokens]
- Monthly cost: [$]
- Model: [name]

**Growth Projections:**
- Document growth: [% per month]
- Query growth: [% per month]
- New use cases planned: [description]

**Budget Constraints:**
- Maximum acceptable monthly cost: [$]
- When this becomes a problem: [month/date]

Please provide:
1. Cost projection curve (6, 12, 24 months)
2. When budget will be exceeded
3. Optimization levers to pull
4. Alternative architectures for scale
5. Phased approach to manage costs
```

---

## Usage Tips

### For Best Results

1. **Be specific** - Include actual numbers, not vague descriptions
2. **Provide context** - Explain your constraints and goals
3. **Share examples** - Include sample queries and documents when relevant
4. **List what you've tried** - Mention failed approaches to avoid redundant suggestions
5. **Specify priorities** - Rank quality vs cost vs latency importance

### Follow-up Questions

After getting initial recommendations, consider asking:

- "What are the risks of this approach?"
- "How would this change if [constraint] were different?"
- "Can you provide a code example for implementing this?"
- "What monitoring should I set up to validate this?"
- "What's the rollback plan if this doesn't work?"

---

*These prompts are designed for use with Claude, GPT-4, or similar LLMs. Adjust specificity based on your needs.*
