# RAG Evaluation

## Overview

RAG evaluation measures the quality of retrieval and generation components separately and together. This methodology covers metrics, evaluation frameworks, and techniques for building reliable RAG systems.

## When to Use

- Validating RAG pipeline before production
- Comparing different retrieval strategies
- Tuning chunk sizes and overlap
- Selecting embedding models
- Measuring generation quality
- Continuous monitoring in production

## Key Concepts

### Evaluation Dimensions

| Dimension | Measures | Key Metrics |
|-----------|----------|-------------|
| Retrieval | Finding relevant docs | Precision, Recall, MRR, NDCG |
| Generation | Response quality | Faithfulness, Relevance, Coherence |
| End-to-End | Full pipeline | Answer accuracy, User satisfaction |

### RAG Triad (RAGAS Framework)

```
CONTEXT RELEVANCE
(Is retrieved context relevant to the question?)
        |
        v
+-------+-------+
|               |
v               v
FAITHFULNESS    ANSWER RELEVANCE
(Is answer      (Does answer
grounded in     address the
context?)       question?)
```

## Metrics Deep Dive

### Retrieval Metrics

| Metric | Description | Target | Formula |
|--------|-------------|--------|---------|
| **Precision@K** | How many retrieved docs are relevant? | > 0.7 | relevant_in_top_k / k |
| **Recall@K** | How many relevant docs were retrieved? | > 0.8 | relevant_retrieved / total_relevant |
| **MRR** | How highly is the first relevant doc ranked? | > 0.6 | 1 / rank_of_first_relevant |
| **NDCG@K** | Graded relevance with position weighting | > 0.8 | DCG / IDCG |
| **Hit Rate** | Was at least one relevant doc retrieved? | > 0.9 | 1 if any relevant else 0 |

**Why Position Matters:**
- LLMs have context window limits
- Positional bias affects which content gets used
- Relevant docs buried at position 10+ may be ignored

### Generation Metrics

| Metric | Description | Target | Evaluator |
|--------|-------------|--------|-----------|
| **Faithfulness** | Is answer grounded in retrieved context? | > 0.85 | LLM-as-judge |
| **Answer Relevance** | Does answer address the question? | > 0.9 | LLM-as-judge |
| **Context Relevance** | Is retrieved context relevant? | > 0.7 | LLM-as-judge |
| **Hallucination Rate** | Unsupported or fabricated claims | < 0.1 | LLM-as-judge |
| **Citation Coverage** | Are claims backed with sources? | > 0.8 | Rule-based |

### Composite Metrics

| Metric | Components | Use Case |
|--------|------------|----------|
| **RAGAS Score** | Faithfulness + Relevance + Context | Overall RAG quality |
| **Answer Correctness** | Semantic similarity + Factual overlap | Against ground truth |
| **Context Precision** | Relevant chunks / Total chunks | Retrieval efficiency |

## Evaluation Frameworks

### RAGAS (Primary)

Open-source framework for RAG evaluation with reference-free metrics.

**Metrics Available:**
- `faithfulness` - Grounded in context
- `answer_relevancy` - Addresses question
- `context_precision` - Relevant chunks ranked first
- `context_recall` - All relevant info retrieved
- `context_entity_recall` - Entity coverage
- `answer_similarity` - Semantic match to ground truth
- `answer_correctness` - Factual correctness

**Best For:** Initial assessment, no reference data needed

### Other Frameworks

| Framework | Strength | Best For |
|-----------|----------|----------|
| **ARES** | Adversarial testing | Stress-testing retrieval |
| **LangSmith** | LLM-as-judge, tracing | Production monitoring |
| **AWS Bedrock Eval** | Native AWS integration | AWS deployments |
| **Vertex AI Eval** | GCP integration | GCP deployments |
| **DeepEval** | Comprehensive metrics | Detailed analysis |
| **TruLens** | Feedback functions | Iteration tracking |

## Best Practices

### Ground Truth Creation

1. Manually verify answers
2. Include diverse question types (factual, comparative, reasoning)
3. Cover edge cases
4. Document source passages

### Metric Selection

| Situation | Metrics to Use |
|-----------|----------------|
| Have relevance labels | Precision, Recall, NDCG, MRR |
| No ground truth | Faithfulness, Relevance (LLM-based) |
| Production monitoring | Latency + Faithfulness + Hit Rate |
| Model comparison | Full RAGAS suite |

### Evaluation Frequency

| Phase | Frequency | Metrics |
|-------|-----------|---------|
| Development | Every change | Full suite |
| Staging | Daily | Core metrics |
| Production | Continuous | Lightweight + sampling |

### Human Evaluation

- Sample 5-10% of outputs for manual review
- Create annotation guidelines
- Calculate inter-annotator agreement (Cohen's Kappa > 0.7)
- Focus on hallucination detection

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| No ground truth | Can't measure accuracy | Use LLM-based metrics |
| Single metric | Over-optimization | Use multiple metrics |
| Non-representative test set | Production gaps | Sample from real queries |
| Evaluator bias | LLM has preferences | Use multiple evaluators |
| Ignoring latency | Only quality, not speed | Add P95 latency metric |
| Static evaluation | Stale after changes | Automate in CI/CD |

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts |
| [checklist.md](checklist.md) | Evaluation checklist |
| [examples.md](examples.md) | Code examples |
| [templates.md](templates.md) | Evaluation templates |
| [llm-prompts.md](llm-prompts.md) | LLM evaluation prompts |

## References

- [RAGAS Documentation](https://docs.ragas.io/)
- [RAGAS Paper](https://arxiv.org/abs/2309.15217)
- [RAG Evaluation - Pinecone](https://www.pinecone.io/learn/rag-evaluation/)
- [RAG Evaluation - Qdrant](https://qdrant.tech/blog/rag-evaluation-guide/)
- [LlamaIndex Evaluation](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/)

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Retrieval metrics | sonnet | Evaluation framework |
| Generation quality | sonnet | Quality assessment |
| End-to-end evaluation | sonnet | System evaluation |
