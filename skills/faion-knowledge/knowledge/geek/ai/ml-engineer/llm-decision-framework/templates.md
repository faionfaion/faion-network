# LLM Architecture Templates

Reusable templates for LLM architecture decisions and documentation.

## Template 1: Architecture Decision Record (ADR)

```markdown
# ADR-XXX: LLM Enhancement Strategy for [Feature/System]

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Date

YYYY-MM-DD

## Context

[Describe the problem or requirement that needs LLM enhancement]

### Requirements

| Requirement | Value |
|-------------|-------|
| Data freshness | [Real-time | Daily | Static] |
| Data volume | [Number of documents/records] |
| Latency | [Target response time] |
| Accuracy | [Target accuracy percentage] |
| Volume | [Queries per day] |
| Citations | [Required | Not required] |
| Output format | [Free-form | Structured JSON | Domain-specific] |

### Constraints

| Constraint | Value |
|------------|-------|
| Budget (setup) | [$X] |
| Budget (monthly) | [$X/month] |
| Team expertise | [None | Basic | Advanced] |
| Timeline | [Days | Weeks | Months] |
| Privacy | [Public cloud | Private cloud | On-premise] |

## Decision

We will use **[Prompt Engineering | RAG | Fine-tuning | RAFT (Hybrid)]** because:

1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

### Architecture

```
[ASCII diagram of data flow]
```

### Components

| Component | Choice | Rationale |
|-----------|--------|-----------|
| LLM Provider | [OpenAI | Claude | etc.] | [Why] |
| Model | [GPT-4o | Claude 3.5 | etc.] | [Why] |
| Vector DB | [Qdrant | Pinecone | etc.] | [Why] |
| Embedding | [ada-002 | e5-large | etc.] | [Why] |
| Framework | [LangChain | LlamaIndex | etc.] | [Why] |

## Alternatives Considered

### Alternative 1: [Name]

**Pros:** [List]
**Cons:** [List]
**Why rejected:** [Explanation]

### Alternative 2: [Name]

**Pros:** [List]
**Cons:** [List]
**Why rejected:** [Explanation]

## Consequences

### Positive

- [Benefit 1]
- [Benefit 2]

### Negative

- [Tradeoff 1]
- [Tradeoff 2]

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | [Low/Med/High] | [Low/Med/High] | [Plan] |

## Cost Estimate

| Item | Setup | Monthly |
|------|-------|---------|
| Infrastructure | $X | $X |
| LLM API | $0 | $X |
| Vector DB | $X | $X |
| Observability | $0 | $X |
| **Total** | **$X** | **$X** |

## Implementation Plan

1. [ ] Phase 1: [Description]
2. [ ] Phase 2: [Description]
3. [ ] Phase 3: [Description]

## References

- [Link to relevant documentation]
- [Link to similar implementations]
```

---

## Template 2: RAG Architecture Specification

```markdown
# RAG Architecture: [System Name]

## Overview

[Brief description of the RAG system purpose]

## Data Sources

| Source | Type | Update Frequency | Volume |
|--------|------|------------------|--------|
| [Source 1] | [DB/API/Files] | [Real-time/Daily/etc.] | [X docs] |
| [Source 2] | [DB/API/Files] | [Real-time/Daily/etc.] | [X docs] |

## Ingestion Pipeline

### Document Processing

```yaml
chunking:
  strategy: [fixed | semantic | recursive]
  size: [500-1000]
  overlap: [50-100]

preprocessing:
  - remove_headers: true
  - extract_tables: true
  - ocr_images: [true | false]
```

### Embedding

```yaml
model: [text-embedding-3-small | e5-large-v2 | etc.]
dimensions: [256 | 512 | 1024 | 1536]
batch_size: 100
```

## Retrieval Pipeline

### Query Processing

```yaml
query_expansion: [true | false]
hyde: [true | false]  # Hypothetical Document Embeddings
query_decomposition: [true | false]
```

### Search Strategy

```yaml
vector_search:
  top_k: 10
  similarity: [cosine | dot_product | euclidean]

hybrid_search:
  enabled: [true | false]
  bm25_weight: 0.3
  vector_weight: 0.7

reranking:
  enabled: [true | false]
  model: [cohere-rerank | cross-encoder | etc.]
  top_n: 5
```

## Generation

### LLM Configuration

```yaml
provider: [openai | anthropic | etc.]
model: [gpt-4o | claude-3-5-sonnet | etc.]
temperature: 0.1
max_tokens: 1024
```

### Prompt Template

```
You are a helpful assistant that answers questions based on the provided context.

Context:
{context}

Question: {question}

Instructions:
1. Answer based only on the provided context
2. If the context doesn't contain the answer, say "I don't have enough information"
3. Cite your sources using [Source: document_name]

Answer:
```

## Infrastructure

```yaml
vector_database:
  type: [qdrant | pinecone | weaviate | pgvector]
  deployment: [cloud | self-hosted]
  resources:
    memory: [X GB]
    storage: [X GB]

caching:
  type: [redis | memcached | none]
  ttl: [X seconds]

observability:
  tracing: [langfuse | langsmith | none]
  metrics: [prometheus | cloudwatch | none]
```

## Evaluation Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Retrieval recall@5 | >90% | [Weekly evaluation] |
| Answer accuracy | >85% | [LLM-as-judge] |
| Latency P95 | <2s | [Real-time monitoring] |
| Hallucination rate | <5% | [Human evaluation] |

## Fallback Strategy

```yaml
primary:
  provider: openai
  model: gpt-4o

fallback:
  - provider: anthropic
    model: claude-3-5-sonnet
  - provider: openai
    model: gpt-4o-mini

circuit_breaker:
  failure_threshold: 5
  recovery_timeout: 60s
```
```

---

## Template 3: Fine-tuning Specification

```markdown
# Fine-tuning Specification: [Model Name]

## Objective

[What specific behavior or capability should the fine-tuned model have?]

## Base Model

| Property | Value |
|----------|-------|
| Provider | [OpenAI | Anthropic | HuggingFace] |
| Model | [GPT-4o | Llama 3.2 | etc.] |
| Context window | [X tokens] |
| Parameters | [X B] |

## Training Data

### Dataset Overview

| Metric | Value |
|--------|-------|
| Total examples | [X] |
| Training set | [X] (80%) |
| Validation set | [X] (10%) |
| Test set | [X] (10%) |
| Avg input tokens | [X] |
| Avg output tokens | [X] |

### Data Format

```json
{
  "messages": [
    {"role": "system", "content": "[System prompt]"},
    {"role": "user", "content": "[User input]"},
    {"role": "assistant", "content": "[Desired output]"}
  ]
}
```

### Data Quality Criteria

- [ ] No PII or sensitive data
- [ ] Consistent formatting
- [ ] High-quality outputs
- [ ] Representative of production distribution
- [ ] Edge cases included

## Training Configuration

### Method: [SFT | LoRA | QLoRA | DPO]

```yaml
# For SFT (OpenAI)
hyperparameters:
  n_epochs: 3
  batch_size: auto
  learning_rate_multiplier: auto

# For LoRA (HuggingFace)
lora:
  r: 16
  alpha: 32
  dropout: 0.05
  target_modules: ["q_proj", "v_proj"]
```

## Evaluation

### Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| Accuracy | [X%] | [X%] |
| Format compliance | [X%] | [X%] |
| Domain relevance | [X%] | [X%] |

### Evaluation Methods

1. **Automated metrics:** [Accuracy, F1, BLEU, etc.]
2. **LLM-as-judge:** [Criteria for evaluation]
3. **Human evaluation:** [Evaluation protocol]

## Deployment

```yaml
deployment:
  platform: [OpenAI | HuggingFace | vLLM | TGI]
  resources:
    gpu: [A100 | H100 | etc.]
    memory: [X GB]

monitoring:
  drift_detection: true
  retraining_trigger: [accuracy drop > 5%]
```

## Cost Estimate

| Item | Cost |
|------|------|
| Training compute | $X |
| Evaluation compute | $X |
| Data preparation | $X hours |
| Inference (per 1M tokens) | $X |
| **Total training** | **$X** |
```

---

## Template 4: LLM Comparison Matrix

```markdown
# LLM Comparison for [Use Case]

## Candidates

| Model | Provider | Context | Price (input/output per 1M) |
|-------|----------|---------|----------------------------|
| GPT-4o | OpenAI | 128K | $2.50 / $10.00 |
| Claude 3.5 Sonnet | Anthropic | 200K | $3.00 / $15.00 |
| Gemini 1.5 Pro | Google | 2M | $1.25 / $5.00 |
| [Model 4] | [Provider] | [Context] | [Price] |

## Evaluation Results

### Task-Specific Performance

| Metric | GPT-4o | Claude 3.5 | Gemini 1.5 | [Model 4] |
|--------|--------|------------|------------|-----------|
| Task accuracy | X% | X% | X% | X% |
| Format compliance | X% | X% | X% | X% |
| Latency (avg) | Xms | Xms | Xms | Xms |
| Cost per query | $X | $X | $X | $X |

### Qualitative Assessment

| Factor | GPT-4o | Claude 3.5 | Gemini 1.5 |
|--------|--------|------------|------------|
| Instruction following | [1-5] | [1-5] | [1-5] |
| Reasoning quality | [1-5] | [1-5] | [1-5] |
| Output consistency | [1-5] | [1-5] | [1-5] |
| Safety/alignment | [1-5] | [1-5] | [1-5] |

## Recommendation

**Selected model:** [Model Name]

**Rationale:**
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

**Fallback:** [Model Name] for [specific scenarios]
```

---

## Template 5: Cost Analysis Worksheet

```markdown
# LLM Cost Analysis: [Project Name]

## Volume Estimates

| Metric | Current | 6 Months | 12 Months |
|--------|---------|----------|-----------|
| Queries/day | X | X | X |
| Avg input tokens | X | X | X |
| Avg output tokens | X | X | X |

## Option 1: [Approach Name]

### Cost Breakdown

| Component | Unit Cost | Monthly Units | Monthly Cost |
|-----------|-----------|---------------|--------------|
| LLM API (input) | $X/1M | X M | $X |
| LLM API (output) | $X/1M | X M | $X |
| Vector DB | $X/month | 1 | $X |
| Embeddings | $X/1M | X M | $X |
| Infrastructure | $X/month | 1 | $X |
| **Total** | | | **$X** |

### With Optimizations

| Optimization | Savings | New Monthly Cost |
|--------------|---------|------------------|
| Semantic caching (40% hit rate) | -$X | $X |
| Prompt compression | -$X | $X |
| Smaller model for simple queries | -$X | $X |
| **Optimized Total** | | **$X** |

## Option 2: [Approach Name]

[Repeat structure]

## TCO Comparison (12 months)

| Option | Setup | Year 1 Operational | Total TCO |
|--------|-------|-------------------|-----------|
| Option 1 | $X | $X | $X |
| Option 2 | $X | $X | $X |
| Option 3 | $X | $X | $X |

## Recommendation

[Based on cost analysis, recommend approach with rationale]
```

---

*LLM Architecture Templates v2.0*
