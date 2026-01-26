# RAG Evaluation Templates

## Test Set Template

### JSON Format

```json
{
  "test_set_id": "ts-001",
  "created_at": "2025-01-15",
  "version": "1.0",
  "description": "Production RAG evaluation test set",
  "questions": [
    {
      "id": "q-001",
      "question": "What is the return policy for electronics?",
      "type": "factual",
      "difficulty": "easy",
      "ground_truth": "Electronics can be returned within 30 days with original packaging.",
      "relevant_doc_ids": ["doc-123", "doc-456"],
      "relevance_grades": {
        "doc-123": 3,
        "doc-456": 2,
        "doc-789": 1
      },
      "source_quote": "All electronic items are eligible for return within 30 days of purchase, provided they are in original packaging.",
      "tags": ["policy", "returns", "electronics"]
    },
    {
      "id": "q-002",
      "question": "How does the loyalty program compare to competitors?",
      "type": "comparative",
      "difficulty": "hard",
      "ground_truth": "Our loyalty program offers 2x points vs industry average of 1x, plus exclusive member-only sales.",
      "relevant_doc_ids": ["doc-200", "doc-201", "doc-202"],
      "relevance_grades": {
        "doc-200": 3,
        "doc-201": 3,
        "doc-202": 2
      },
      "tags": ["loyalty", "comparison", "benefits"]
    }
  ],
  "metadata": {
    "total_questions": 2,
    "by_type": {
      "factual": 1,
      "comparative": 1
    },
    "by_difficulty": {
      "easy": 1,
      "hard": 1
    }
  }
}
```

### CSV Format

```csv
id,question,type,difficulty,ground_truth,relevant_doc_ids,tags
q-001,What is the return policy for electronics?,factual,easy,"Electronics can be returned within 30 days with original packaging.","doc-123,doc-456","policy,returns"
q-002,How does the loyalty program compare to competitors?,comparative,hard,"Our loyalty program offers 2x points vs industry average.","doc-200,doc-201","loyalty,comparison"
```

## Evaluation Report Template

### Markdown Format

```markdown
# RAG Evaluation Report

## Summary

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| Hit Rate | 0.92 | 0.90 | PASS |
| MRR | 0.68 | 0.60 | PASS |
| Precision@5 | 0.74 | 0.70 | PASS |
| NDCG@10 | 0.81 | 0.80 | PASS |
| Faithfulness | 0.87 | 0.85 | PASS |
| Answer Relevance | 0.91 | 0.90 | PASS |

**Overall Status:** PASS (6/6 metrics met)

## Configuration

| Parameter | Value |
|-----------|-------|
| Embedding Model | text-embedding-3-large |
| Vector DB | Qdrant |
| Chunk Size | 512 tokens |
| Chunk Overlap | 50 tokens |
| Top K | 5 |
| LLM | GPT-4o |

## Test Set Details

- Total Questions: 100
- Question Types: Factual (40), Comparative (20), Reasoning (25), Summarization (15)
- Difficulty: Easy (30), Medium (45), Hard (25)

## Retrieval Analysis

### Performance by Question Type

| Type | Hit Rate | MRR | Precision@5 |
|------|----------|-----|-------------|
| Factual | 0.95 | 0.78 | 0.82 |
| Comparative | 0.85 | 0.55 | 0.65 |
| Reasoning | 0.92 | 0.62 | 0.70 |
| Summarization | 0.90 | 0.70 | 0.75 |

### Failure Analysis

**Zero Results (3 queries):**
- q-045: Rare terminology not in index
- q-067: Misspelled query
- q-089: Out-of-domain question

**Low Relevance (8 queries):**
- Common issue: Semantic similarity matched wrong context
- Recommendation: Add negative examples to training

## Generation Analysis

### Performance by Metric

| Metric | Mean | Std | Min | Max |
|--------|------|-----|-----|-----|
| Faithfulness | 0.87 | 0.12 | 0.45 | 1.00 |
| Answer Relevance | 0.91 | 0.08 | 0.60 | 1.00 |
| Context Relevance | 0.78 | 0.15 | 0.30 | 1.00 |

### Hallucination Analysis

**Hallucinations Detected:** 5/100 (5%)

| Query ID | Type | Description |
|----------|------|-------------|
| q-012 | Fabricated fact | Invented date not in context |
| q-034 | Extrapolation | Extended claim beyond context |
| q-056 | Wrong number | Incorrect statistic |
| q-078 | Attribution | Attributed to wrong source |
| q-091 | Confusion | Mixed up two similar concepts |

## Recommendations

1. **Improve Retrieval for Comparative Questions**
   - Add cross-document retrieval
   - Implement query expansion

2. **Reduce Hallucinations**
   - Add "I don't know" capability
   - Implement citation requirements

3. **Increase Context Relevance**
   - Tune chunk size (try 256 tokens)
   - Add re-ranking step

## Next Steps

- [ ] Implement query expansion for comparative questions
- [ ] Add re-ranker (Cohere or cross-encoder)
- [ ] Test smaller chunk sizes
- [ ] Add confidence scoring

## Appendix

### Raw Scores by Query

[Link to detailed CSV]

### Configuration History

| Date | Change | Impact |
|------|--------|--------|
| 2025-01-01 | Baseline | - |
| 2025-01-08 | Increased top_k to 5 | +5% recall |
| 2025-01-15 | Added re-ranker | +8% precision |
```

## A/B Test Report Template

```markdown
# A/B Test Report: [Experiment Name]

## Hypothesis

**If** we [change X], **then** [metric Y] will [improve/decrease] **because** [reasoning].

## Configurations

### Control (A)

| Parameter | Value |
|-----------|-------|
| Chunk Size | 512 |
| Top K | 5 |
| Re-ranker | None |

### Treatment (B)

| Parameter | Value |
|-----------|-------|
| Chunk Size | 256 |
| Top K | 10 |
| Re-ranker | Cohere |

## Results

### Primary Metrics

| Metric | Control (A) | Treatment (B) | Delta | p-value |
|--------|-------------|---------------|-------|---------|
| Faithfulness | 0.82 | 0.89 | +8.5% | 0.003 |
| MRR | 0.65 | 0.72 | +10.8% | 0.001 |
| Latency (P95) | 1.2s | 1.8s | +50% | <0.001 |

### Secondary Metrics

| Metric | Control (A) | Treatment (B) | Delta |
|--------|-------------|---------------|-------|
| Token Usage | 2,500 | 3,200 | +28% |
| Cost/Query | $0.012 | $0.018 | +50% |

## Statistical Analysis

- Sample Size: 500 queries
- Confidence Level: 95%
- Test Duration: 7 days

### Significance

| Metric | Significant? | Winner |
|--------|--------------|--------|
| Faithfulness | Yes (p=0.003) | B |
| MRR | Yes (p=0.001) | B |
| Latency | Yes (p<0.001) | A |

## Conclusion

**Winner:** Treatment (B) for quality metrics, but with latency/cost tradeoff.

**Decision:** Implement Treatment (B) with following modifications:
- Add caching to reduce latency
- Set token budget to limit cost

## Rollout Plan

1. [ ] Stage 1: 10% traffic (1 week)
2. [ ] Stage 2: 50% traffic (1 week)
3. [ ] Stage 3: 100% traffic
```

## Evaluation Pipeline Config Template

### YAML Format

```yaml
# rag-eval-config.yaml

evaluation:
  name: "Production RAG Evaluation"
  version: "1.0.0"

test_set:
  path: "./test_sets/production-v1.json"
  sample_size: null  # null = use all
  stratify_by: "type"  # ensure balanced types

retrieval_metrics:
  enabled: true
  metrics:
    - name: "hit_rate"
      target: 0.90
    - name: "mrr"
      target: 0.60
    - name: "precision_at_k"
      k: 5
      target: 0.70
    - name: "recall_at_k"
      k: 5
      target: 0.80
    - name: "ndcg_at_k"
      k: 10
      target: 0.80

generation_metrics:
  enabled: true
  evaluator_model: "gpt-4o"
  metrics:
    - name: "faithfulness"
      target: 0.85
    - name: "answer_relevance"
      target: 0.90
    - name: "context_relevance"
      target: 0.70

ragas:
  enabled: true
  metrics:
    - "faithfulness"
    - "answer_relevancy"
    - "context_precision"
    - "context_recall"

output:
  format: "markdown"
  path: "./reports/eval-{timestamp}.md"
  include_raw_scores: true

alerts:
  enabled: true
  channels:
    - type: "slack"
      webhook: "${SLACK_WEBHOOK_URL}"
    - type: "email"
      recipients: ["team@example.com"]
  triggers:
    - metric: "faithfulness"
      condition: "below"
      threshold: 0.80
    - metric: "hit_rate"
      condition: "below"
      threshold: 0.85
```

## Ground Truth Annotation Template

### Guidelines Document

```markdown
# Ground Truth Annotation Guidelines

## Annotator Instructions

### Task

For each question, provide:
1. The correct answer
2. Relevant document IDs
3. Relevance grades for each document

### Relevance Scale

| Grade | Description | Example |
|-------|-------------|---------|
| 3 | Highly relevant | Contains direct answer |
| 2 | Relevant | Contains supporting info |
| 1 | Marginally relevant | Tangentially related |
| 0 | Not relevant | No useful information |

### Answer Quality Criteria

**Good Answer:**
- Directly addresses the question
- Factually accurate
- Concise but complete
- Uses information from documents only

**Bad Answer:**
- Tangential to question
- Contains speculation
- Overly verbose
- Includes external knowledge

### Edge Cases

**Unanswerable Questions:**
- Mark as `ground_truth: null`
- Note reason: "out_of_scope" or "insufficient_context"

**Multiple Valid Answers:**
- Provide primary answer
- List alternatives in `alternative_answers` field

### Quality Checks

- [ ] Answer is factually verifiable
- [ ] All relevant docs are identified
- [ ] Relevance grades are consistent
- [ ] Source quote supports answer
```

## Monitoring Dashboard Config

```yaml
# grafana-dashboard.yaml

dashboard:
  title: "RAG Evaluation Metrics"
  refresh: "5m"

panels:
  - title: "Faithfulness (7-day rolling)"
    type: "graph"
    query: "avg(rag_faithfulness) by (day)"
    thresholds:
      - value: 0.85
        color: "green"
      - value: 0.70
        color: "yellow"
      - value: 0.0
        color: "red"

  - title: "MRR by Question Type"
    type: "bar"
    query: "avg(rag_mrr) by (question_type)"

  - title: "Latency P95"
    type: "gauge"
    query: "histogram_quantile(0.95, rag_latency_seconds)"
    max: 5
    thresholds:
      - value: 1
        color: "green"
      - value: 2
        color: "yellow"
      - value: 5
        color: "red"

  - title: "Hallucination Rate"
    type: "stat"
    query: "sum(rag_hallucinations) / sum(rag_total_queries)"
    format: "percent"

alerts:
  - name: "Faithfulness Drop"
    condition: "avg(rag_faithfulness) < 0.80 for 1h"
    severity: "warning"

  - name: "High Hallucination Rate"
    condition: "rag_hallucination_rate > 0.15 for 30m"
    severity: "critical"
```
